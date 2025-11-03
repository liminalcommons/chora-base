# React Configuration Templates

This directory contains reusable configuration templates for React projects using SAP-020.

## Available Templates

### TypeScript Configurations

- **tsconfig.strict.json** - Maximum type safety (recommended for production)
- **tsconfig.relaxed.json** - Easier for learning/prototyping

### Usage

Copy the desired config to your project:

```bash
# Use strict config (recommended)
cp templates/react/configs/tsconfig.strict.json my-project/tsconfig.json

# Or use relaxed config for learning
cp templates/react/configs/tsconfig.relaxed.json my-project/tsconfig.json
```

## Configuration Philosophy

SAP-020 strongly recommends **strict mode** for all production projects:
- Catches 40% more errors at compile time
- Better IDE autocomplete and refactoring
- Industry standard (78% adoption)

Relaxed mode is provided only for:
- Learning React/TypeScript
- Quick prototypes
- Migration from JavaScript

**Always migrate to strict mode before production deployment.**
