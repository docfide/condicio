const Ajv = require('ajv/dist/2020.js')
const addFormats = require('ajv-formats')
const yaml = require('js-yaml')
const fs = require('fs')
const path = require('path')

const schema = require('../schema/condicio.schema.json')
const examplesDir = path.join(__dirname, '..', 'schema', 'examples')

const ajv = new Ajv()
addFormats(ajv)
const validate = ajv.compile(schema)

const files = fs.readdirSync(examplesDir)
let allValid = true

for (const file of files) {
  const ext = path.extname(file)
  const filePath = path.join(examplesDir, file)

  let doc
  if (ext === '.json') {
    doc = require(filePath)
  } else if (ext === '.yaml' || ext === '.yml') {
    doc = yaml.load(fs.readFileSync(filePath, 'utf8'))
  } else {
    continue
  }

  const valid = validate(doc)
  if (valid) {
    console.log(`  PASS  ${file}`)
  } else {
    console.log(`  FAIL  ${file}`)
    console.log(`        ${JSON.stringify(validate.errors)}`)
    allValid = false
  }
}

if (allValid) {
  console.log('\nAll examples pass validation.')
  process.exit(0)
} else {
  console.log('\nSome examples failed validation.')
  process.exit(1)
}
