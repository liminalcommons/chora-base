#!/usr/bin/env node

/**
 * Bundle Analysis Script
 *
 * SAP-025: React Performance Optimization
 *
 * This script analyzes your production bundle and provides:
 * - Bundle size breakdown (JS, CSS, images, fonts)
 * - Largest files in each category
 * - Recommendations for optimization
 * - Size comparisons against budgets
 *
 * Usage:
 *   node scripts/analyze-bundle.js [--framework=nextjs|vite]
 *
 * Examples:
 *   node scripts/analyze-bundle.js --framework=nextjs
 *   node scripts/analyze-bundle.js --framework=vite
 */

const fs = require('fs')
const path = require('path')

// ============================================
// CONFIGURATION
// ============================================

const FRAMEWORK = process.argv.includes('--framework=vite') ? 'vite' : 'nextjs'

const BUILD_DIR = {
  nextjs: '.next',
  vite: 'dist',
}[FRAMEWORK]

const BUDGETS = {
  script: 200 * 1024, // 200 KB
  stylesheet: 50 * 1024, // 50 KB
  image: 300 * 1024, // 300 KB
  font: 100 * 1024, // 100 KB
  total: 750 * 1024, // 750 KB
}

// ============================================
// COLORS (for terminal output)
// ============================================

const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
}

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Format bytes to human-readable size
 */
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(decimals))} ${sizes[i]}`
}

/**
 * Get file size
 */
function getFileSize(filePath) {
  try {
    return fs.statSync(filePath).size
  } catch (error) {
    return 0
  }
}

/**
 * Get all files in directory recursively
 */
function getAllFiles(dirPath, arrayOfFiles = []) {
  const files = fs.readdirSync(dirPath)

  files.forEach((file) => {
    const filePath = path.join(dirPath, file)

    if (fs.statSync(filePath).isDirectory()) {
      arrayOfFiles = getAllFiles(filePath, arrayOfFiles)
    } else {
      arrayOfFiles.push(filePath)
    }
  })

  return arrayOfFiles
}

/**
 * Categorize file by extension
 */
function categorizeFile(filePath) {
  const ext = path.extname(filePath).toLowerCase()

  if (['.js', '.mjs', '.jsx'].includes(ext)) return 'script'
  if (['.css'].includes(ext)) return 'stylesheet'
  if (['.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.svg', '.ico'].includes(ext))
    return 'image'
  if (['.woff', '.woff2', '.ttf', '.otf', '.eot'].includes(ext)) return 'font'
  if (['.json', '.map'].includes(ext)) return 'other'

  return 'unknown'
}

/**
 * Get status color based on size vs budget
 */
function getStatusColor(size, budget) {
  const percentage = (size / budget) * 100

  if (percentage <= 80) return colors.green
  if (percentage <= 100) return colors.yellow
  return colors.red
}

/**
 * Get status symbol
 */
function getStatusSymbol(size, budget) {
  const percentage = (size / budget) * 100

  if (percentage <= 80) return '✓'
  if (percentage <= 100) return '⚠'
  return '✗'
}

// ============================================
// ANALYZE BUNDLE
// ============================================

function analyzeBundle() {
  console.log(`\n${colors.bright}${colors.cyan}=== Bundle Analysis (${FRAMEWORK.toUpperCase()}) ===${colors.reset}\n`)

  // Check if build directory exists
  if (!fs.existsSync(BUILD_DIR)) {
    console.error(`${colors.red}Error: Build directory "${BUILD_DIR}" not found.${colors.reset}`)
    console.log(`${colors.dim}Run "npm run build" first.${colors.reset}\n`)
    process.exit(1)
  }

  // Get all files
  const allFiles = getAllFiles(BUILD_DIR)

  // Categorize files
  const categories = {
    script: [],
    stylesheet: [],
    image: [],
    font: [],
    other: [],
    unknown: [],
  }

  allFiles.forEach((filePath) => {
    const category = categorizeFile(filePath)
    const size = getFileSize(filePath)

    categories[category].push({
      path: filePath,
      size,
      name: path.basename(filePath),
    })
  })

  // Calculate totals
  const totals = {
    script: categories.script.reduce((sum, file) => sum + file.size, 0),
    stylesheet: categories.stylesheet.reduce((sum, file) => sum + file.size, 0),
    image: categories.image.reduce((sum, file) => sum + file.size, 0),
    font: categories.font.reduce((sum, file) => sum + file.size, 0),
    other: categories.other.reduce((sum, file) => sum + file.size, 0),
    unknown: categories.unknown.reduce((sum, file) => sum + file.size, 0),
  }

  totals.total = Object.values(totals).reduce((sum, size) => sum + size, 0)

  // Print summary
  console.log(`${colors.bright}📦 Bundle Size Summary${colors.reset}\n`)

  Object.entries(totals).forEach(([category, size]) => {
    const budget = BUDGETS[category]
    const color = budget ? getStatusColor(size, budget) : colors.cyan
    const symbol = budget ? getStatusSymbol(size, budget) : ' '
    const percentage = budget ? ` (${Math.round((size / budget) * 100)}%)` : ''

    console.log(
      `  ${symbol} ${category.padEnd(12)} ${color}${formatBytes(size)}${colors.reset}${colors.dim}${percentage}${colors.reset}`
    )
  })

  console.log()

  // Print top files per category
  Object.entries(categories).forEach(([category, files]) => {
    if (files.length === 0 || category === 'other' || category === 'unknown') return

    console.log(`${colors.bright}📄 Top ${category} files${colors.reset}\n`)

    const sortedFiles = files.sort((a, b) => b.size - a.size).slice(0, 5)

    sortedFiles.forEach((file, index) => {
      const relativePath = path.relative(BUILD_DIR, file.path)
      const size = formatBytes(file.size)

      console.log(`  ${index + 1}. ${colors.dim}${relativePath}${colors.reset} - ${colors.cyan}${size}${colors.reset}`)
    })

    console.log()
  })

  // Print recommendations
  console.log(`${colors.bright}💡 Recommendations${colors.reset}\n`)

  let hasIssues = false

  Object.entries(totals).forEach(([category, size]) => {
    const budget = BUDGETS[category]

    if (budget && size > budget) {
      hasIssues = true
      const overage = size - budget
      const percentage = Math.round((size / budget) * 100)

      console.log(
        `  ${colors.red}✗${colors.reset} ${category} exceeds budget by ${colors.red}${formatBytes(overage)}${colors.reset} (${percentage}%)`
      )

      // Category-specific recommendations
      if (category === 'script') {
        console.log(`    ${colors.dim}→ Use code splitting with React.lazy()${colors.reset}`)
        console.log(`    ${colors.dim}→ Remove unused dependencies${colors.reset}`)
        console.log(`    ${colors.dim}→ Use dynamic imports for heavy libraries${colors.reset}`)
      } else if (category === 'stylesheet') {
        console.log(`    ${colors.dim}→ Remove unused CSS with PurgeCSS${colors.reset}`)
        console.log(`    ${colors.dim}→ Use critical CSS for above-the-fold content${colors.reset}`)
      } else if (category === 'image') {
        console.log(`    ${colors.dim}→ Use AVIF/WebP formats${colors.reset}`)
        console.log(`    ${colors.dim}→ Optimize images with next/image or sharp${colors.reset}`)
        console.log(`    ${colors.dim}→ Use responsive images with srcset${colors.reset}`)
      } else if (category === 'font') {
        console.log(`    ${colors.dim}→ Use WOFF2 format${colors.reset}`)
        console.log(`    ${colors.dim}→ Subset fonts to include only needed characters${colors.reset}`)
        console.log(`    ${colors.dim}→ Limit font weights (each weight = separate file)${colors.reset}`)
      }

      console.log()
    }
  })

  if (!hasIssues) {
    console.log(`  ${colors.green}✓${colors.reset} All categories within budget! 🎉\n`)
  }

  // Print budget status
  console.log(`${colors.bright}📊 Budget Status${colors.reset}\n`)

  Object.entries(BUDGETS).forEach(([category, budget]) => {
    const size = totals[category]
    const percentage = Math.round((size / budget) * 100)
    const color = getStatusColor(size, budget)
    const symbol = getStatusSymbol(size, budget)

    // Progress bar
    const barLength = 30
    const filled = Math.min(Math.round((size / budget) * barLength), barLength)
    const bar = '█'.repeat(filled) + '░'.repeat(barLength - filled)

    console.log(
      `  ${symbol} ${category.padEnd(12)} ${color}${bar}${colors.reset} ${percentage}%`
    )
  })

  console.log()

  // Exit with error if budgets exceeded
  if (hasIssues) {
    console.log(`${colors.red}${colors.bright}⚠ Bundle size exceeds budgets!${colors.reset}\n`)
    process.exit(1)
  } else {
    console.log(`${colors.green}${colors.bright}✓ Bundle size within budgets!${colors.reset}\n`)
  }
}

// ============================================
// RUN
// ============================================

analyzeBundle()
