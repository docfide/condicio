const schema = require('../schema/condicio.schema.json')
const fs = require('fs')
const path = require('path')

const DOCS_DIR = path.join(__dirname, '..', 'docs')

function describeProperty(name, prop, required, depth = 0) {
  const lines = []
  const indent = '  '.repeat(depth)
  const req = required?.includes(name) ? ' **required**' : ''
  const type = prop.type || (prop.oneOf ? prop.oneOf.map(t => t.type || t.$ref?.split('/').pop()).join(' | ') : prop.$ref?.split('/').pop() || 'any')
  const enum_ = prop.enum ? ` \`${prop.enum.join('`, `')}\`` : ''
  const examples_ = prop.examples ? ` (e.g. ${prop.examples.map(e => `\`${JSON.stringify(e)}\``).join(', ')})` : ''
  const ref = prop.$ref ? ` (see [$#${prop.$ref.split('#')[1] || ''}#](${prop.$ref.split('/').pop()}))` : ''

  lines.push(`${indent}- **\`${name}\`**${req} — ${prop.description || ''}${type ? ` *${type}*` : ''}${enum_}${examples_}${ref}`)

  if (prop.properties) {
    const subRequired = prop.required || []
    for (const [k, v] of Object.entries(prop.properties)) {
      lines.push(describeProperty(k, v, subRequired, depth + 1))
    }
  }
  if (prop.items) {
    if (prop.items.properties) {
      const itemRequired = prop.items.required || []
      for (const [k, v] of Object.entries(prop.items.properties)) {
        lines.push(describeProperty(k, v, itemRequired, depth + 1))
      }
    }
    if (prop.items.$ref) {
      const defName = prop.items.$ref.split('/').pop()
      lines.push(`${indent}  - Items: [$#{$defs/${defName}}](#${defName})`)
    }
  }
  if (prop.oneOf) {
    for (let i = 0; i < prop.oneOf.length; i++) {
      const opt = prop.oneOf[i]
      if (opt.properties) {
        const subRequired = opt.required || []
        for (const [k, v] of Object.entries(opt.properties)) {
          lines.push(describeProperty(k, v, subRequired, depth + 1))
        }
      }
      if (opt.$ref) {
        const defName = opt.$ref.split('/').pop()
        lines.push(`${indent}  - Option: [$#{$defs/${defName}}](#${defName})`)
      }
    }
  }
  return lines.join('\n')
}

function generateFieldReference() {
  const lines = []
  lines.push('# Field Reference')
  lines.push('')
  lines.push('Auto-generated from [`schema/condicio.schema.json`](../schema/condicio.schema.json).')
  lines.push('')
  lines.push('## Root-level fields')
  lines.push('')

  const rootRequired = schema.required || []
  for (const [name, prop] of Object.entries(schema.properties || {})) {
    lines.push(describeProperty(name, prop, rootRequired))
    lines.push('')
  }

  lines.push('---')
  lines.push('')
  lines.push('## Defined types (`$defs`)')
  lines.push('')

  for (const [name, def] of Object.entries(schema.$defs || {})) {
    lines.push(`### ${name}`)
    lines.push('')
    lines.push(`${def.description || ''}`)
    lines.push('')

    if (def.oneOf) {
      lines.push(`One of the following:`)
      lines.push('')
      for (let i = 0; i < def.oneOf.length; i++) {
        const opt = def.oneOf[i]
        lines.push(`**Option ${i + 1}:** ${opt.description || opt.type || opt.$ref?.split('/').pop() || ''}`)
        lines.push('')
        if (opt.properties) {
          const req = opt.required || []
          for (const [k, v] of Object.entries(opt.properties)) {
            lines.push(describeProperty(k, v, req, 0))
          }
        }
        if (opt.$ref) {
          lines.push(`  - *See [${opt.$ref.split('/').pop()}](#${opt.$ref.split('/').pop()})*`)
        }
        lines.push('')
      }
    } else {
      if (def.type === 'object' && def.properties) {
        const req = def.required || []
        for (const [k, v] of Object.entries(def.properties)) {
          lines.push(describeProperty(k, v, req, 0))
        }
      } else if (def.type === 'string' && def.enum) {
        lines.push(`Allowed values: \`${def.enum.join('`, `')}\``)
      } else if (def.type === 'string') {
        lines.push(`Type: \`string\`${def.examples ? ` — e.g. ${def.examples.map(e => `\`${e}\``).join(', ')}` : ''}`)
      } else {
        const req = def.required || []
        if (def.properties) {
          for (const [k, v] of Object.entries(def.properties)) {
            lines.push(describeProperty(k, v, req, 0))
          }
        }
      }
    }
    lines.push('')
    lines.push('---')
    lines.push('')
  }

  return lines.join('\n')
}

const fieldRef = generateFieldReference()
fs.writeFileSync(path.join(DOCS_DIR, 'field-reference.md'), fieldRef)
console.log('Generated docs/field-reference.md')
