#!/usr/bin/env node

const { spawn } = require('child_process')
const path = require('path')

console.log('🚀 Starting Vue.js Development Server with Hot Reload...')

// Set development environment
process.env.NODE_ENV = 'development'
process.env.VUE_APP_ENV = 'development'

// Start the development server
const child = spawn('npm', ['run', 'dev'], {
  stdio: 'inherit',
  shell: true,
  cwd: __dirname
})

child.on('close', (code) => {
  console.log(`Development server exited with code ${code}`)
  process.exit(code)
})

child.on('error', (error) => {
  console.error('Failed to start development server:', error)
  process.exit(1)
})

// Handle process termination
process.on('SIGINT', () => {
  console.log('\n🛑 Stopping development server...')
  child.kill('SIGINT')
})

process.on('SIGTERM', () => {
  console.log('\n🛑 Stopping development server...')
  child.kill('SIGTERM')
})
