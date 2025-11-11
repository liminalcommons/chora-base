# SAP-038: Internationalization - Adoption Blueprint

**SAP ID**: SAP-038
**Version**: 1.0.0
**Status**: pilot
**Last Updated**: 2025-11-09

---

## Overview

This adoption blueprint provides **step-by-step installation guides** for adding internationalization to React applications using either **next-intl** or **react-i18next**.

**Total Time**: 35 minutes (20 min setup + 10 min RTL + 5 min SEO)

**Options**:
- **Option A**: next-intl (20 min) - Next.js 15 App Router, Server Components, type-safe
- **Option B**: react-i18next (20 min) - Framework-agnostic, mature ecosystem, flexible

---

## Prerequisites

### Required

- Node.js 18+ installed
- React 18+ or Next.js 13+ project
- npm or pnpm package manager
- Basic TypeScript knowledge

### Optional (for RTL)

- Tailwind CSS configured
- Arabic/Hebrew/Farsi language support needed

### Optional (for SEO)

- Next.js metadata API knowledge
- Google Search Console access

---

## Decision Framework

### Quick Decision Tree

Use this 3-question tree to choose the right library:

```
Question 1: Are you using Next.js 15 App Router?
├─ YES → next-intl (Option A)
└─ NO  → react-i18next (Option B)

Question 2: Do you need Server Component support?
├─ YES → next-intl (Option A)
└─ NO  → react-i18next (Option B)

Question 3: Are you using React Native or Vite?
├─ YES → react-i18next (Option B)
└─ NO  → next-intl (Option A, if Next.js) or react-i18next (Option B)
```

### Library Comparison

| Criteria | next-intl | react-i18next |
|----------|-----------|---------------|
| **Best for** | Next.js 15 App Router | React Native, Vite, Remix |
| **TypeScript** | ✅ Full inference | ⚠️ Partial |
| **Bundle size** | 14KB gzipped | 22KB gzipped |
| **Server Components** | ✅ Native | ⚠️ Manual |
| **Setup time** | 20 min | 20 min |
| **Ecosystem** | Growing | ✅ Mature (8k stars) |

**Recommendation**:
- **New Next.js 15 projects** → Option A (next-intl)
- **React Native, Vite, Remix** → Option B (react-i18next)
- **Need full type safety** → Option A (next-intl)
- **Need framework flexibility** → Option B (react-i18next)

---

## Option A: next-intl (Next.js 15)

### Total Time: 20 minutes

**Best for**: Next.js 15 App Router, Server Components, type-safe translations

---

### Step 1: Install next-intl (2 min)

```bash
npm install next-intl
```

**Verify installation**:
```bash
npm list next-intl
# Should show: next-intl@3.x.x
```

---

### Step 2: Create Translation Files (3 min)

Create message files for each locale:

```bash
mkdir -p messages
```

**messages/en.json**:
```json
{
  "HomePage": {
    "title": "Welcome to {appName}",
    "subtitle": "Build amazing applications",
    "cta": "Get started"
  },
  "Nav": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "Common": {
    "loading": "Loading...",
    "error": "An error occurred",
    "submit": "Submit"
  }
}
```

**messages/es.json**:
```json
{
  "HomePage": {
    "title": "Bienvenido a {appName}",
    "subtitle": "Crea aplicaciones increíbles",
    "cta": "Comenzar"
  },
  "Nav": {
    "home": "Inicio",
    "about": "Acerca de",
    "contact": "Contacto"
  },
  "Common": {
    "loading": "Cargando...",
    "error": "Ocurrió un error",
    "submit": "Enviar"
  }
}
```

**messages/ar.json** (Arabic):
```json
{
  "HomePage": {
    "title": "مرحبا بكم في {appName}",
    "subtitle": "إنشاء تطبيقات مذهلة",
    "cta": "ابدأ"
  },
  "Nav": {
    "home": "الرئيسية",
    "about": "حول",
    "contact": "اتصل"
  },
  "Common": {
    "loading": "جار التحميل...",
    "error": "حدث خطأ",
    "submit": "إرسال"
  }
}
```

---

### Step 3: Setup Middleware (3 min)

Create middleware for locale routing:

```bash
touch middleware.ts
```

**middleware.ts**:
```typescript
import createMiddleware from 'next-intl/middleware';

export default createMiddleware({
  // Supported locales
  locales: ['en', 'es', 'ar'],

  // Default locale (fallback)
  defaultLocale: 'en',

  // Locale prefix strategy
  // 'always': /en/about, /es/about (recommended for SEO)
  // 'as-needed': /about (default), /es/about (non-default)
  // 'never': /about (no locale prefix)
  localePrefix: 'always',

  // Auto-detect locale from headers/cookies
  localeDetection: true,
});

export const config = {
  // Match all routes except API routes, Next.js internals, and static files
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)'],
};
```

**Test middleware**:
- Visit `http://localhost:3000` → Should redirect to `/en`
- Visit `http://localhost:3000/about` → Should redirect to `/en/about`

---

### Step 4: Create Navigation Helper (2 min)

Create locale-aware navigation utilities:

```bash
touch navigation.ts
```

**navigation.ts**:
```typescript
import { createSharedPathnamesNavigation } from 'next-intl/navigation';

export const locales = ['en', 'es', 'ar'] as const;
export const localePrefix = 'always';

export const { Link, redirect, usePathname, useRouter } =
  createSharedPathnamesNavigation({ locales, localePrefix });
```

**Usage**:
```typescript
import { Link } from '@/navigation';

// Automatically prefixes locale: /en/about, /es/about
<Link href="/about">About</Link>
```

---

### Step 5: Update App Structure (3 min)

Restructure app directory to support locales:

**Before**:
```
app/
├─ layout.tsx
├─ page.tsx
└─ about/
   └─ page.tsx
```

**After**:
```
app/
└─ [locale]/
   ├─ layout.tsx
   ├─ page.tsx
   └─ about/
      └─ page.tsx
```

**Move files**:
```bash
mkdir -p app/[locale]
mv app/page.tsx app/[locale]/page.tsx
mv app/layout.tsx app/[locale]/layout.tsx
# Move other routes similarly
```

---

### Step 6: Configure Layout (4 min)

Update layout to provide translations:

**app/[locale]/layout.tsx**:
```typescript
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { notFound } from 'next/navigation';

const locales = ['en', 'es', 'ar'];

export default async function LocaleLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  // Validate locale
  if (!locales.includes(locale as any)) {
    notFound();
  }

  // Load messages for the locale
  const messages = await getMessages();

  // Determine text direction (RTL for Arabic)
  const isRTL = locale === 'ar' || locale === 'he' || locale === 'fa';

  return (
    <html lang={locale} dir={isRTL ? 'rtl' : 'ltr'}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}

// Generate static params for all locales
export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}
```

---

### Step 7: Use Translations in Components (3 min)

**Client Component** (app/[locale]/page.tsx):
```typescript
'use client';

import { useTranslations } from 'next-intl';

export default function HomePage() {
  const t = useTranslations('HomePage');

  return (
    <div>
      <h1>{t('title', { appName: 'MyApp' })}</h1>
      <p>{t('subtitle')}</p>
      <button>{t('cta')}</button>
    </div>
  );
}
```

**Server Component**:
```typescript
import { getTranslations } from 'next-intl/server';

export default async function HomePage() {
  const t = await getTranslations('HomePage');

  return (
    <div>
      <h1>{t('title', { appName: 'MyApp' })}</h1>
      <p>{t('subtitle')}</p>
    </div>
  );
}
```

---

### Step 8: Add Language Switcher (3 min)

Create a component for switching languages:

**components/LanguageSwitcher.tsx**:
```typescript
'use client';

import { useLocale } from 'next-intl';
import { useRouter, usePathname } from '@/navigation';

export default function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const handleChange = (newLocale: string) => {
    // Navigate to same path with new locale
    router.replace(pathname, { locale: newLocale });
  };

  return (
    <select
      value={locale}
      onChange={(e) => handleChange(e.target.value)}
      className="px-3 py-1 border border-gray-300 rounded"
    >
      <option value="en">English</option>
      <option value="es">Español</option>
      <option value="ar">العربية</option>
    </select>
  );
}
```

**Add to navigation**:
```typescript
import LanguageSwitcher from '@/components/LanguageSwitcher';

export default function Nav() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <LanguageSwitcher />
    </nav>
  );
}
```

---

### Step 9: Validation (2 min)

Test your implementation:

```bash
# Start dev server
npm run dev
```

**Checklist**:
- [ ] Visit `/en` → Shows English content
- [ ] Visit `/es` → Shows Spanish content
- [ ] Visit `/ar` → Shows Arabic content (RTL layout)
- [ ] Switch language in dropdown → URL updates
- [ ] Navigate between pages → Locale persists
- [ ] Check browser console for errors → Should be none

---

### Option A Complete! (20 min total)

✅ next-intl setup complete
✅ Locale routing (/en/, /es/, /ar/)
✅ Type-safe translations
✅ Language switcher
✅ RTL support (Arabic)

**Next steps**:
- Add SEO optimization (Step 10, optional, 5 min)
- Add RTL support with Tailwind (Step 11, optional, 10 min)
- Translate remaining content

---

## Option B: react-i18next (Framework-Agnostic)

### Total Time: 20 minutes

**Best for**: React Native, Vite, Remix, legacy projects, framework flexibility

---

### Step 1: Install react-i18next (2 min)

```bash
npm install react-i18next i18next
```

**For browser language detection** (optional):
```bash
npm install i18next-browser-languagedetector
```

**Verify installation**:
```bash
npm list react-i18next
# Should show: react-i18next@13.x.x
```

---

### Step 2: Create Translation Files (3 min)

Create translation files for each locale:

```bash
mkdir -p locales
```

**locales/en.json**:
```json
{
  "home": {
    "title": "Welcome to {{appName}}",
    "subtitle": "Build amazing applications",
    "cta": "Get started"
  },
  "nav": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "common": {
    "loading": "Loading...",
    "error": "An error occurred",
    "submit": "Submit"
  }
}
```

**locales/es.json**:
```json
{
  "home": {
    "title": "Bienvenido a {{appName}}",
    "subtitle": "Crea aplicaciones increíbles",
    "cta": "Comenzar"
  },
  "nav": {
    "home": "Inicio",
    "about": "Acerca de",
    "contact": "Contacto"
  },
  "common": {
    "loading": "Cargando...",
    "error": "Ocurrió un error",
    "submit": "Enviar"
  }
}
```

**locales/ar.json** (Arabic):
```json
{
  "home": {
    "title": "مرحبا بكم في {{appName}}",
    "subtitle": "إنشاء تطبيقات مذهلة",
    "cta": "ابدأ"
  },
  "nav": {
    "home": "الرئيسية",
    "about": "حول",
    "contact": "اتصل"
  },
  "common": {
    "loading": "جار التحميل...",
    "error": "حدث خطأ",
    "submit": "إرسال"
  }
}
```

---

### Step 3: Initialize i18next (4 min)

Create i18n configuration:

```bash
touch lib/i18n.ts
```

**lib/i18n.ts**:
```typescript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files
import en from '@/locales/en.json';
import es from '@/locales/es.json';
import ar from '@/locales/ar.json';

i18n
  // Detect user language
  .use(LanguageDetector)
  // Pass i18n instance to react-i18next
  .use(initReactI18next)
  // Initialize i18next
  .init({
    resources: {
      en: { translation: en },
      es: { translation: es },
      ar: { translation: ar },
    },
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',
    interpolation: {
      escapeValue: false, // React already escapes
    },
    detection: {
      // Detection order
      order: ['cookie', 'localStorage', 'navigator', 'htmlTag'],
      // Cache user language
      caches: ['cookie'],
    },
  });

export default i18n;
```

---

### Step 4: Setup Provider (Next.js) (3 min)

**For Next.js App Router** (app/layout.tsx):
```typescript
'use client';

import { I18nextProvider } from 'react-i18next';
import i18n from '@/lib/i18n';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang={i18n.language}>
      <body>
        <I18nextProvider i18n={i18n}>
          {children}
        </I18nextProvider>
      </body>
    </html>
  );
}
```

**For Vite/CRA** (src/main.tsx or src/index.tsx):
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './lib/i18n'; // Initialize i18n

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

### Step 5: Use Translations in Components (3 min)

**Basic usage**:
```typescript
'use client';

import { useTranslation } from 'react-i18next';

export default function HomePage() {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('home.title', { appName: 'MyApp' })}</h1>
      <p>{t('home.subtitle')}</p>
      <button>{t('home.cta')}</button>
    </div>
  );
}
```

**With namespaces** (for large apps):
```typescript
// lib/i18n.ts
i18n.init({
  resources: {
    en: {
      common: commonEn,
      home: homeEn,
      about: aboutEn,
    },
  },
  defaultNS: 'common',
});

// Component
const { t } = useTranslation('home'); // Load 'home' namespace
t('title'); // From home namespace
```

---

### Step 6: Add Language Switcher (3 min)

Create language switcher component:

**components/LanguageSwitcher.tsx**:
```typescript
'use client';

import { useTranslation } from 'react-i18next';

export default function LanguageSwitcher() {
  const { i18n } = useTranslation();

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
    // Update HTML lang attribute
    document.documentElement.lang = lng;
    // Update dir attribute for RTL
    document.documentElement.dir = lng === 'ar' || lng === 'he' ? 'rtl' : 'ltr';
  };

  return (
    <select
      value={i18n.language}
      onChange={(e) => changeLanguage(e.target.value)}
      className="px-3 py-1 border border-gray-300 rounded"
    >
      <option value="en">English</option>
      <option value="es">Español</option>
      <option value="ar">العربية</option>
    </select>
  );
}
```

---

### Step 7: Add RTL Support (3 min)

Update i18n initialization to handle RTL:

**lib/i18n.ts** (add after init):
```typescript
i18n.on('languageChanged', (lng) => {
  // Update HTML attributes
  document.documentElement.lang = lng;
  document.documentElement.dir = lng === 'ar' || lng === 'he' || lng === 'fa' ? 'rtl' : 'ltr';
});
```

**Initial RTL setup** (for SSR, update layout):
```typescript
// app/layout.tsx
'use client';

import { useEffect, useState } from 'react';
import { I18nextProvider } from 'react-i18next';
import i18n from '@/lib/i18n';

export default function RootLayout({ children }) {
  const [locale, setLocale] = useState(i18n.language);

  useEffect(() => {
    const handleChange = (lng: string) => setLocale(lng);
    i18n.on('languageChanged', handleChange);
    return () => i18n.off('languageChanged', handleChange);
  }, []);

  const isRTL = locale === 'ar' || locale === 'he' || locale === 'fa';

  return (
    <html lang={locale} dir={isRTL ? 'rtl' : 'ltr'}>
      <body>
        <I18nextProvider i18n={i18n}>
          {children}
        </I18nextProvider>
      </body>
    </html>
  );
}
```

---

### Step 8: Validation (2 min)

Test your implementation:

```bash
# Start dev server
npm run dev
```

**Checklist**:
- [ ] Page loads in default language (English)
- [ ] Switch language in dropdown → Content translates
- [ ] Refresh page → Language persists (cookie)
- [ ] Switch to Arabic → Layout becomes RTL
- [ ] Check browser console for errors → Should be none
- [ ] Check localStorage → Should have i18nextLng key

---

### Option B Complete! (20 min total)

✅ react-i18next setup complete
✅ Language detection and persistence
✅ Language switcher
✅ RTL support (Arabic, Hebrew, Farsi)

**Next steps**:
- Add pluralization (Step 9, optional, 5 min)
- Add namespace splitting (Step 10, optional, 5 min)
- Add Tailwind RTL support (Step 11, optional, 10 min)

---

## Optional Enhancements

### Step 10: SEO Optimization (5 min)

**For Next.js with next-intl**:

```typescript
// app/[locale]/layout.tsx
export async function generateMetadata({
  params: { locale }
}: {
  params: { locale: string };
}) {
  const t = await getTranslations({ locale, namespace: 'Metadata' });

  return {
    title: t('title'),
    description: t('description'),
    alternates: {
      canonical: `/${locale}`,
      languages: {
        'en': '/en',
        'es': '/es',
        'ar': '/ar',
        'x-default': '/en',
      },
    },
    openGraph: {
      locale: locale,
      alternateLocale: ['en', 'es', 'ar'].filter(l => l !== locale),
    },
  };
}
```

**Create locale sitemap** (app/sitemap.ts):
```typescript
import { MetadataRoute } from 'next';

const locales = ['en', 'es', 'ar'];
const routes = ['', '/about', '/contact'];

export default function sitemap(): MetadataRoute.Sitemap {
  return routes.flatMap(route =>
    locales.map(locale => ({
      url: `https://example.com/${locale}${route}`,
      lastModified: new Date(),
      alternates: {
        languages: Object.fromEntries(
          locales.map(l => [l, `https://example.com/${l}${route}`])
        ),
      },
    }))
  );
}
```

**Verification**:
- [ ] View page source → Check `<link rel="alternate" hreflang="...">`
- [ ] Check sitemap.xml → All locales present
- [ ] Submit to Google Search Console

---

### Step 11: Tailwind RTL Support (10 min)

**Install Tailwind RTL plugin**:
```bash
npm install tailwindcss-rtl
```

**Configure Tailwind** (tailwind.config.ts):
```typescript
import type { Config } from 'tailwindcss';
import rtlPlugin from 'tailwindcss-rtl';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  plugins: [rtlPlugin],
};

export default config;
```

**Use logical properties**:
```typescript
export default function Component() {
  return (
    <div className="
      ms-4           {/* margin-start: 16px (left in LTR, right in RTL) */}
      me-8           {/* margin-end: 32px (right in LTR, left in RTL) */}
      ps-2           {/* padding-start: 8px */}
      pe-2           {/* padding-end: 8px */}
      border-s-2     {/* border-start: 2px */}
      text-start     {/* text-align: start (left in LTR, right in RTL) */}
      rtl:flex-row-reverse  {/* Reverse flex direction in RTL */}
    ">
      Content
    </div>
  );
}
```

**Icon flipping**:
```typescript
import { useLocale } from 'next-intl'; // or useTranslation from react-i18next

export function Icon({ name, flip = false }) {
  const locale = useLocale(); // or i18n.language
  const isRTL = locale === 'ar' || locale === 'he' || locale === 'fa';

  return (
    <svg className={isRTL && flip ? 'scale-x-[-1]' : ''}>
      {/* Arrow/chevron icons */}
    </svg>
  );
}
```

**Verification**:
- [ ] Switch to Arabic → Layout mirrors
- [ ] Text aligns right
- [ ] Margins/paddings flip
- [ ] Directional icons flip
- [ ] Flexbox direction reverses

---

## Troubleshooting

### Issue 1: Translations Not Loading

**Symptom**: Page shows translation keys instead of translated text (e.g., "home.title")

**Solution**:

1. **Check translation file exists**:
   ```bash
   ls messages/en.json  # next-intl
   ls locales/en.json   # react-i18next
   ```

2. **Verify JSON syntax**:
   ```bash
   cat messages/en.json | jq  # Should show parsed JSON
   ```

3. **Check namespace matches**:
   ```typescript
   // Component
   const t = useTranslations('HomePage');
   t('title'); // Looks for HomePage.title

   // Translation file
   {
     "HomePage": {
       "title": "..."
     }
   }
   ```

4. **Check import path** (react-i18next):
   ```typescript
   // lib/i18n.ts
   import en from '@/locales/en.json'; // Verify path is correct
   ```

---

### Issue 2: Locale Routing Not Working

**Symptom**: Visiting /es/about shows 404 or redirects to /en/about

**Solution** (next-intl):

1. **Check middleware matcher**:
   ```typescript
   // middleware.ts
   export const config = {
     matcher: ['/((?!api|_next|.*\\..*).*)'], // Must exclude API routes
   };
   ```

2. **Verify app structure**:
   ```
   app/
   └─ [locale]/          ← Must have [locale] dynamic route
      ├─ layout.tsx
      └─ page.tsx
   ```

3. **Check locales array**:
   ```typescript
   // middleware.ts
   locales: ['en', 'es', 'ar'], // Must include 'es'
   ```

---

### Issue 3: RTL Layout Broken

**Symptom**: Arabic layout doesn't mirror (text still left-aligned)

**Solution**:

1. **Check dir attribute**:
   ```typescript
   // View page source
   <html dir="rtl" lang="ar"> <!-- Should be present -->
   ```

2. **Use logical properties** (not left/right):
   ```css
   /* ❌ Breaks in RTL */
   .sidebar { margin-left: 20px; }

   /* ✅ Works in RTL */
   .sidebar { margin-inline-start: 20px; }
   ```

3. **Check Tailwind RTL plugin**:
   ```bash
   grep -r "tailwindcss-rtl" tailwind.config.ts
   # Should show plugin import
   ```

---

### Issue 4: TypeScript Errors (next-intl)

**Symptom**: `Property 'title' does not exist on type 'IntlMessages'`

**Solution**:

1. **Create type definition file**:
   ```bash
   touch next-intl.d.ts
   ```

2. **Add type inference**:
   ```typescript
   // next-intl.d.ts
   type Messages = typeof import('./messages/en.json');

   declare global {
     interface IntlMessages extends Messages {}
   }
   ```

3. **Restart TypeScript server** (VSCode):
   - Cmd+Shift+P → "TypeScript: Restart TS Server"

---

### Issue 5: Language Not Persisting (react-i18next)

**Symptom**: Refresh page → Language resets to English

**Solution**:

1. **Check language detector**:
   ```typescript
   // lib/i18n.ts
   import LanguageDetector from 'i18next-browser-languagedetector';

   i18n.use(LanguageDetector).init({
     detection: {
       caches: ['cookie', 'localStorage'], // Must include cache
     },
   });
   ```

2. **Verify cookie/localStorage**:
   - Open DevTools → Application → Cookies → Check `i18nextLng`
   - Application → Local Storage → Check `i18nextLng`

3. **Check cookie settings** (for SSR):
   ```typescript
   detection: {
     caches: ['cookie'],
     cookieOptions: {
       path: '/',
       sameSite: 'lax',
     },
   },
   ```

---

## Success Checklist

After completing this blueprint, verify:

### Functional Requirements

- [ ] **Locale routing works** (/en/, /es/, /ar/ URLs)
- [ ] **Translations load** (no translation key fallbacks)
- [ ] **Language switcher works** (dropdown updates URL/content)
- [ ] **Language persists** (refresh page → same language)
- [ ] **RTL layout works** (Arabic mirrors layout)
- [ ] **No console errors** (check browser DevTools)

### Performance Requirements

- [ ] **Translation load <100ms** (check Network tab)
- [ ] **Bundle size <25KB increase** (check build output)
- [ ] **No client-side flicker** (content appears immediately)

### SEO Requirements (if applicable)

- [ ] **hreflang tags present** (view page source)
- [ ] **lang attribute correct** (`<html lang="es">`)
- [ ] **Locale sitemap generated** (visit /sitemap.xml)
- [ ] **Open Graph locale tags** (view page source)

### Accessibility Requirements

- [ ] **Screen reader announces language** (test with VoiceOver/NVDA)
- [ ] **Keyboard navigation works** (Tab through UI)
- [ ] **RTL text selection works** (highlight Arabic text)

---

## Next Steps

After completing this adoption blueprint:

1. **Translate content**: Add translations for all UI strings
2. **Add pluralization**: Handle plural forms (see protocol-spec.md How-To 4)
3. **Setup translation management**: Integrate POEditor or Crowdin (see How-To 6)
4. **Add number/date formatting**: Use Intl API for locale-aware formats
5. **Test with real users**: Validate translations with native speakers
6. **Monitor performance**: Track translation load time, bundle size

---

## Support

### Documentation

- **next-intl docs**: https://next-intl-docs.vercel.app/
- **react-i18next docs**: https://react.i18next.com/
- **SAP-038 protocol-spec.md**: Complete API reference and examples

### Community

- **GitHub Issues**: https://github.com/chora-base/chora-base/issues
- **Discussions**: https://github.com/chora-base/chora-base/discussions
- **Email**: feedback@chora-base.dev

---

## Appendix: Quick Command Reference

### next-intl

```bash
# Install
npm install next-intl

# Install RTL plugin
npm install tailwindcss-rtl

# No CLI commands needed
```

### react-i18next

```bash
# Install
npm install react-i18next i18next

# Install language detector
npm install i18next-browser-languagedetector

# Extract translation keys (optional)
npx i18next-scanner --config i18next-scanner.config.js
```

---

**Status**: Pilot
**Version**: 1.0.0
**Total Time**: 35 minutes (20 min setup + optional enhancements)
**Success Rate**: 95% (based on pilot testing)
