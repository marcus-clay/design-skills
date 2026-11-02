// Builds what is derived from the catalogue, so nothing is counted or listed by hand:
//   node scripts/build.mjs          checks the skills and rewrites the index in README.md
//   node scripts/build.mjs --zip    also writes dist/<skill>.zip for every skill of this repository
// The curated data lives in catalog/skills.json; the skills themselves live in skills/<id>/SKILL.md.
import fs from 'fs'
import path from 'path'
import { execFileSync } from 'child_process'

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..')
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog/skills.json'), 'utf8'))
const REPO = 'marcus-clay/design-skills'

// 1. Check: every skill of the repository has a SKILL.md whose name is its folder name
const problems = []
const local = catalog.skills.filter((s) => !s.repo)
for (const s of local) {
  const file = path.join(root, 'skills', s.id, 'SKILL.md')
  if (!fs.existsSync(file)) {
    problems.push(`skills/${s.id}/SKILL.md manque`)
    continue
  }
  const name = fs.readFileSync(file, 'utf8').match(/^name:\s*(.+)$/m)?.[1]?.trim()
  if (name !== s.id) problems.push(`skills/${s.id}/SKILL.md déclare name: ${name}`)
}
for (const dir of fs.readdirSync(path.join(root, 'skills'), { withFileTypes: true })) {
  if (dir.isDirectory() && !catalog.skills.some((s) => s.id === dir.name)) problems.push(`skills/${dir.name} n'est pas dans catalog/skills.json`)
}
const known = new Set([...catalog.skills.map((s) => s.id), ...catalog.external.map((s) => s.id)])
for (const s of catalog.skills) for (const d of s.dependsOn ?? []) if (!known.has(d)) problems.push(`${s.id} dépend de ${d}, absent du catalogue`)
for (const s of [...catalog.skills, ...catalog.external]) for (const t of s.themes) if (!catalog.themes.includes(t)) problems.push(`${s.id} : thème inconnu « ${t} »`)
if (problems.length) {
  console.error(problems.map((p) => `- ${p}`).join('\n'))
  process.exit(1)
}

// 2. Index: one table per theme, own skills first, then recommended ones
const fr = (t) => t.replace(/ ([:;?!\u00bb])/g, "\u00a0$1").replace(/\u00ab /g, "\u00ab\u00a0")
const link = (text, url) => (url ? `[${text}](${url})` : text)
const titleOf = (id) => catalog.external.find((e) => e.id === id)?.title ?? id
const rows = (theme) => {
  const own = catalog.skills
    .filter((s) => s.themes.includes(theme))
    .map((s) => {
      const where = s.repo ? link('dépôt dédié', s.repo) + (s.site ? `, ${link('démos', s.site)}` : '') : link('dossier', `skills/${s.id}`)
      const needs = s.dependsOn?.length ? ` S'appuie sur ${s.dependsOn.map(titleOf).join(' et ')}.` : ''
      return `| \`${s.id}\` | ${s.summary}${needs} | ${where} |`
    })
  const ext = catalog.external
    .filter((s) => s.themes.includes(theme))
    .map((s) => `| ${s.title} | ${s.summary}${s.names ? ` (${s.names.length} skills)` : ''} | ${link(`recommandée, par ${s.author}`, s.site ?? s.repo)} |`)
  return [...own, ...ext]
}
const index = catalog.themes
  .map((t) => {
    const r = rows(t)
    return r.length ? `### ${t}\n\n| Skill | Ce qu'elle fait | Où |\n|---|---|---|\n${r.join('\n')}` : ''
  })
  .filter(Boolean)
  .join('\n\n')

const readmePath = path.join(root, 'README.md')
let readme = fs.readFileSync(readmePath, 'utf8')
const block = `<!-- index:start -->\n${fr(index)}\n<!-- index:end -->`
if (!/<!-- index:start -->[\s\S]*<!-- index:end -->/.test(readme)) {
  console.error('README.md : repères index:start / index:end introuvables')
  process.exit(1)
}
readme = readme.replace(/<!-- index:start -->[\s\S]*<!-- index:end -->/, block)

// The recommended skills: author, source, licence and the command their own page gives
const externalBlock = catalog.external
  .map((s) => {
    const lines = [`### ${s.title}`, '', `Par ${s.author}${s.license ? `, licence ${s.license}` : ''}. ${[s.repo && link('Dépôt', s.repo), s.site && link('Site', s.site)].filter(Boolean).join(' · ')}`]
    if (s.install) lines.push('', '```bash', s.install, '```')
    if (s.names?.length) lines.push('', `<details><summary>${s.names.length} skills de cette collection retenues ici</summary>`, '', s.names.map((n) => `\`${n}\``).join(', '), '', '</details>')
    if (s.note) lines.push('', s.note)
    return lines.join('\n')
  })
  .join('\n\n')
if (!/<!-- external:start -->[\s\S]*<!-- external:end -->/.test(readme)) {
  console.error('README.md : repères external:start / external:end introuvables')
  process.exit(1)
}
readme = readme.replace(/<!-- external:start -->[\s\S]*<!-- external:end -->/, `<!-- external:start -->\n${fr(externalBlock)}\n<!-- external:end -->`)
fs.writeFileSync(readmePath, readme)
console.log(`Index à jour : ${local.length} skills dans ce dépôt, ${catalog.skills.length - local.length} dans un dépôt dédié, ${catalog.external.length} recommandées.`)

// 3. Archives for claude.ai: dist/<id>.zip with the skill folder at the root
if (process.argv.includes('--zip')) {
  const dist = path.join(root, 'dist')
  fs.mkdirSync(dist, { recursive: true })
  for (const f of fs.readdirSync(dist)) if (f.endsWith(".zip")) fs.unlinkSync(path.join(dist, f))
  for (const s of local) {
    const out = path.join(dist, `${s.id}.zip`)
    if (fs.existsSync(out)) fs.unlinkSync(out)
    execFileSync('zip', ['-qr', out, s.id, '-x', '*.DS_Store'], { cwd: path.join(root, 'skills') })
  }
  console.log(`Archives écrites dans dist/ (${local.length}). Publication : gh release create <tag> dist/*.zip --repo ${REPO}`)
}
