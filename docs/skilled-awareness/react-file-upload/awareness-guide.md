# SAP-035: React File Upload - Awareness Guide (AGENTS.md)

**SAP ID**: SAP-035
**Name**: react-file-upload
**Full Name**: React File Upload & Storage
**Status**: pilot
**Version**: 1.0.0
**Created**: 2025-11-09
**Last Updated**: 2025-11-09
**Diataxis Type**: Explanation

---

## 📖 Quick Reference

**New to SAP-035?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 4-provider decision tree (UploadThing, Vercel Blob, Supabase, AWS S3)
- 📚 **91.7% Time Savings** - 6 hours → 30 minutes with production templates
- 🎯 **Security-First** - 3-layer validation, virus scanning, upload authorization
- 🔧 **Pre-Built Components** - UploadThing `<UploadButton>`, `<UploadDropzone>` (rapid prototyping)
- 📊 **Image Optimization** - Sharp.js integration (WebP, AVIF, resizing, CDN delivery)
- 🔗 **Integration** - Works with SAP-020 (Next.js 15), SAP-033 (Auth), SAP-034 (Database)

This awareness-guide.md provides: Agent-specific file upload workflows, provider selection patterns, and security best practices for AI coding assistants

---

## When to Use This SAP

### Use SAP-035 When

1. **Building apps with file uploads**
   - User avatars, profile pictures
   - Document uploads (PDFs, DOCX)
   - Image galleries, media libraries
   - CSV/Excel imports
   - Video uploads

2. **Need secure file storage**
   - Authenticated uploads only
   - File validation (type, size, MIME)
   - Virus scanning for large files
   - Row-Level Security (RLS) for multi-tenant apps

3. **Want image optimization**
   - Resize images (thumbnail, medium, large)
   - Format conversion (JPEG → WebP → AVIF)
   - Quality compression (30-70% size reduction)
   - Metadata stripping (EXIF removal for privacy)

4. **Require progress indicators**
   - Real-time upload percentage
   - Multi-file batch uploads
   - Large file uploads (>100MB)

5. **Need CDN delivery**
   - Global edge caching
   - <50ms latency worldwide
   - Automatic cache invalidation

---

### Skip SAP-035 When

1. **Simple static file hosting**
   - Use Next.js `public/` folder for static assets
   - No user uploads, just bundled files

2. **No file uploads needed**
   - Pure frontend-only app
   - Static site with no backend

3. **Extreme customization required**
   - Need custom storage backend (not S3/Blob/Supabase)
   - Complex file processing (custom video transcoding pipeline)

---

## Upload Provider Decision Tree

### Quick Decision

```
Choose provider based on:
├─ Using Next.js + want simplicity? → UploadThing
│  └─ Free tier (2GB), type-safe, pre-built UI
├─ Using Vercel + need edge? → Vercel Blob
│  └─ Edge-optimized, global CDN, 3x cost-efficient
├─ Using Supabase + need RLS? → Supabase Storage
│  └─ PostgreSQL integration, image transforms, $0.021/GB
└─ Enterprise + AWS? → AWS S3
   └─ 11 nines durability, compliance, presigned URLs
```

---

### Decision Matrix

| Criteria | UploadThing | Vercel Blob | Supabase Storage | AWS S3 |
|----------|-------------|-------------|------------------|--------|
| **Setup Time** | 20 min | 15 min (fastest) | 20 min | 30 min |
| **Free Tier** | ✅ 2GB | ❌ NO | ✅ 1GB | ✅ 5GB (12mo) |
| **Cost (10GB)** | $10/mo | $15.50/mo | $9.21/mo (cheapest) | $9.23/mo |
| **Max File Size** | 100MB (free) | 500MB | 50MB (free) | 5GB |
| **Pre-Built UI** | ✅ YES | ❌ NO | ❌ NO | ❌ NO |
| **TypeScript** | ✅ Full | ✅ Full | ✅ Full | ⚠️ Verbose |

**Recommendation**:
- **Startup/MVP**: UploadThing (free 2GB, fast setup, pre-built UI)
- **Vercel Deployment**: Vercel Blob (edge-optimized, client-side uploads)
- **Supabase Project**: Supabase Storage (RLS, cheapest at $0.021/GB)
- **Enterprise**: AWS S3 (most mature, compliance certifications)

---

## Common Workflows

### Workflow 1: Simple Image Uploader (15 min)

**Goal**: Upload single image with preview

**Steps**:
1. Install UploadThing: `npm install uploadthing @uploadthing/react`
2. Create file router (`app/api/uploadthing/core.ts`)
3. Add `<UploadButton>` component
4. Display uploaded image

**Code**:
```typescript
// app/api/uploadthing/core.ts
import { createUploadthing } from "uploadthing/next"
import { auth } from "@/auth"

const f = createUploadthing()

export const ourFileRouter = {
  imageUploader: f({ image: { maxFileSize: "4MB" } })
    .middleware(async () => {
      const user = await auth()
      if (!user) throw new Error("Unauthorized")
      return { userId: user.id }
    })
    .onUploadComplete(async ({ metadata, file }) => {
      console.log("Uploaded:", file.url)
    })
}

// app/upload/page.tsx
"use client"
import { UploadButton } from "@/utils/uploadthing"
import { useState } from "react"
import Image from "next/image"

export default function UploadPage() {
  const [url, setUrl] = useState<string | null>(null)

  return (
    <div>
      <UploadButton
        endpoint="imageUploader"
        onClientUploadComplete={(res) => setUrl(res?.[0]?.url || null)}
      />
      {url && <Image src={url} alt="Uploaded" width={400} height={300} />}
    </div>
  )
}
```

**Time**: 15 minutes
**Result**: Working image uploader with preview

---

### Workflow 2: Add File Validation (10 min)

**Goal**: Validate file type and size on client + server

**Steps**:
1. Add client-side validation (Zod schema)
2. Add server-side validation (MIME check, magic bytes)
3. Test with invalid files

**Code**:
```typescript
// Client-side validation
import { z } from 'zod'

const fileSchema = z.object({
  file: z.instanceof(File)
    .refine(file => file.size <= 5 * 1024 * 1024, "File must be < 5MB")
    .refine(file => ['image/jpeg', 'image/png', 'image/webp'].includes(file.type), "Only JPEG, PNG, WebP allowed")
})

function validateFile(file: File) {
  const result = fileSchema.safeParse({ file })
  if (!result.success) {
    return { error: result.error.errors[0].message }
  }
  return { success: true }
}

// Server-side validation
"use server"
import { fileTypeFromBuffer } from 'file-type'

export async function uploadFile(formData: FormData) {
  const file = formData.get('file')
  if (!(file instanceof File)) return { error: 'File required' }

  // Validate size
  if (file.size > 5 * 1024 * 1024) return { error: 'File too large' }

  // Validate MIME (magic bytes, not extension)
  const buffer = Buffer.from(await file.arrayBuffer())
  const type = await fileTypeFromBuffer(buffer)

  if (!type || !['image/jpeg', 'image/png', 'image/webp'].includes(type.mime)) {
    return { error: 'Invalid file type' }
  }

  // Upload...
}
```

**Time**: 10 minutes
**Result**: Validated uploads (client + server)

---

### Workflow 3: Image Optimization (10 min)

**Goal**: Optimize images before storage (resize, format, quality)

**Steps**:
1. Install sharp: `npm install sharp`
2. Create optimization function
3. Process images on upload
4. Generate multiple sizes (thumbnail, medium, large)

**Code**:
```typescript
import sharp from 'sharp'

export async function optimizeImage(buffer: Buffer) {
  return await sharp(buffer)
    .rotate() // Auto-rotate based on EXIF
    .resize(1920, 1080, { fit: 'inside', withoutEnlargement: true })
    .webp({ quality: 85 })
    .withMetadata({ exif: {} }) // Remove EXIF for privacy
    .toBuffer()
}

// Generate multiple sizes
export async function generateImageSizes(buffer: Buffer) {
  const [thumbnail, medium, large] = await Promise.all([
    sharp(buffer).resize(200, 200).webp({ quality: 80 }).toBuffer(),
    sharp(buffer).resize(800, 600).webp({ quality: 85 }).toBuffer(),
    sharp(buffer).resize(1920, 1080).webp({ quality: 90 }).toBuffer()
  ])
  return { thumbnail, medium, large }
}
```

**Time**: 10 minutes
**Result**: Optimized images (30-70% size reduction)

---

### Workflow 4: Multi-File Uploader (20 min)

**Goal**: Upload multiple files with progress indicators

**Steps**:
1. Use `useUploadThing` hook
2. Track upload progress
3. Display progress bars
4. Show uploaded files

**Code**:
```typescript
"use client"
import { useUploadThing } from "@/utils/uploadthing"
import { useState } from "react"

export function MultiFileUploader() {
  const [files, setFiles] = useState<File[]>([])

  const { startUpload, isUploading, uploadProgress } = useUploadThing("imageUploader", {
    onClientUploadComplete: (res) => {
      console.log("Uploaded:", res)
      setFiles([])
    }
  })

  return (
    <div>
      <input
        type="file"
        multiple
        onChange={(e) => setFiles(Array.from(e.target.files || []))}
      />
      <button onClick={() => startUpload(files)} disabled={isUploading}>
        {isUploading ? `Uploading... ${uploadProgress}%` : 'Upload'}
      </button>
      {isUploading && <progress value={uploadProgress} max={100} />}
    </div>
  )
}
```

**Time**: 20 minutes
**Result**: Multi-file uploader with progress

---

## Integration with Other SAPs

### SAP-033 (react-authentication)

**Integration**: Require authentication for uploads

**Pattern**:
```typescript
// UploadThing middleware
.middleware(async () => {
  const user = await auth() // SAP-033
  if (!user) throw new Error("Unauthorized")
  return { userId: user.id }
})

// Vercel Blob API route
export async function POST(request: Request) {
  const session = await auth() // SAP-033
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })
  // Upload...
}

// Supabase Storage RLS
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK (auth.uid() IS NOT NULL);
```

**Why**: Prevents unauthenticated users from wasting storage

---

### SAP-034 (react-database-integration)

**Integration**: Store file metadata in database

**Pattern**:
```typescript
// Save upload metadata
.onUploadComplete(async ({ metadata, file }) => {
  await prisma.upload.create({ // SAP-034
    data: {
      url: file.url,
      key: file.key,
      filename: file.name,
      mimeType: file.type,
      size: file.size,
      userId: metadata.userId
    }
  })
})

// Query user's uploads
export async function getUserUploads(userId: string) {
  return await prisma.upload.findMany({ // SAP-034
    where: { userId },
    orderBy: { createdAt: 'desc' }
  })
}
```

**Why**: Track uploads, query files, delete from database when file deleted

---

### SAP-041 (react-form-validation)

**Integration**: File upload forms with Zod validation

**Pattern**:
```typescript
import { z } from 'zod' // SAP-041
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

const schema = z.object({
  avatar: z.instanceof(File)
    .refine(file => file.size <= 4 * 1024 * 1024, "Max 4MB")
    .refine(file => ['image/jpeg', 'image/png'].includes(file.type), "Only JPEG/PNG")
})

const form = useForm({
  resolver: zodResolver(schema)
})
```

**Why**: Type-safe file validation in forms

---

### SAP-032 (react-performance-optimization)

**Integration**: Image optimization with sharp.js

**Pattern**:
```typescript
// Optimize before upload
.onUploadComplete(async ({ file }) => {
  const buffer = await fetch(file.url).then(r => r.arrayBuffer())
  const optimized = await sharp(Buffer.from(buffer)) // SAP-032
    .resize(1920, 1080)
    .webp({ quality: 85 })
    .toBuffer()

  // Upload optimized version
  await uploadOptimized(optimized)
})
```

**Why**: Reduce storage costs, faster page loads

---

## Security Checklist

### Authentication
- [ ] Upload authorization required (SAP-033: `auth()` check)
- [ ] User ID associated with uploads
- [ ] Rate limiting (max 10 uploads/minute per user)

### Validation
- [ ] Client-side validation (file type, size, count)
- [ ] Server-side validation (MIME check, magic bytes)
- [ ] File size limits enforced (4MB images, 16MB documents)
- [ ] Allowed file types (whitelist, not blacklist)

### Security
- [ ] Virus scanning (ClamAV for files >1MB)
- [ ] Filename sanitization (prevent path traversal)
- [ ] Metadata stripping (remove EXIF from images)
- [ ] Signed URLs (presigned URLs for S3, expiring tokens)
- [ ] Storage permissions (private by default, public opt-in)

### Compliance
- [ ] HTTPS-only uploads
- [ ] Encryption at rest (AES-256)
- [ ] RLS policies (Supabase) or IAM policies (AWS)
- [ ] Audit logs (track uploads, deletions)

---

## Common Pitfalls and Solutions

### Pitfall 1: Client-side validation only

**Problem**: Users can bypass client-side checks via DevTools

**Solution**: Always validate on server

```typescript
// ❌ BAD: Client-only
if (file.size > 4MB) return "Too large"

// ✅ GOOD: Server validation
.middleware(async ({ files }) => {
  if (files[0].size > 4 * 1024 * 1024) {
    throw new Error("File too large")
  }
})
```

**Why**: Security must be server-enforced, not client-suggested

---

### Pitfall 2: No virus scanning

**Problem**: Malware uploaded to server, infects infrastructure

**Solution**: Use ClamAV for virus scanning

```typescript
.onUploadComplete(async ({ file }) => {
  const isClean = await scanFile(file.url)
  if (!isClean) {
    await deleteFile(file.url)
    throw new Error("Virus detected")
  }
})
```

**Why**: Files from users are untrusted, must be scanned

---

### Pitfall 3: Missing progress indicators

**Problem**: Users don't know if upload is working, think it's broken

**Solution**: Use upload progress hooks

```typescript
const { startUpload, isUploading, uploadProgress } = useUploadThing("imageUploader")

{isUploading && <progress value={uploadProgress} max={100} />}
```

**Why**: UX feedback prevents user frustration

---

### Pitfall 4: Large unoptimized images

**Problem**: Slow page load, high storage costs, wasted bandwidth

**Solution**: Optimize with sharp.js before upload

```typescript
.onUploadComplete(async ({ file }) => {
  const optimized = await sharp(file.url)
    .resize(1920, 1080)
    .webp({ quality: 85 })
    .toBuffer()

  await uploadOptimized(optimized)
})
```

**Why**: 30-70% size reduction, faster loads, lower costs

---

### Pitfall 5: No authentication

**Problem**: Anyone can upload files, waste storage, spam server

**Solution**: Require auth in middleware

```typescript
.middleware(async () => {
  const user = await auth()
  if (!user) throw new Error("Unauthorized")
  return { userId: user.id }
})
```

**Why**: Only authenticated users should upload

---

### Pitfall 6: MIME type spoofing

**Problem**: Attacker uploads .exe disguised as .jpg (change extension)

**Solution**: Validate magic bytes, not extension

```typescript
import { fileTypeFromBuffer } from 'file-type'

const buffer = Buffer.from(await file.arrayBuffer())
const type = await fileTypeFromBuffer(buffer)

if (type?.mime !== 'image/jpeg') {
  throw new Error("Invalid file type (MIME spoofing detected)")
}
```

**Why**: File extension can be faked, magic bytes cannot

---

### Pitfall 7: Missing CDN

**Problem**: Slow file delivery, high bandwidth costs

**Solution**: Use provider's built-in CDN

```typescript
// UploadThing: Automatic CDN
// Vercel Blob: Edge storage (CDN-backed)
// Supabase: Built-in CDN
// AWS S3: Set up CloudFront
```

**Why**: Global edge caching, <50ms latency worldwide

---

### Pitfall 8: No database integration

**Problem**: Can't query user's uploads, can't delete orphaned files

**Solution**: Save metadata to database (SAP-034)

```typescript
.onUploadComplete(async ({ metadata, file }) => {
  await prisma.upload.create({
    data: {
      url: file.url,
      userId: metadata.userId,
      size: file.size
    }
  })
})
```

**Why**: Track uploads, delete from DB when file deleted

---

## Troubleshooting Guide

### Issue: "Upload failed" error

**Cause**: File size exceeds limit

**Fix**: Increase `maxFileSize` in file router

```typescript
f({ image: { maxFileSize: "8MB" } }) // Increase from 4MB
```

---

### Issue: "CORS error" when uploading

**Cause**: Missing CORS configuration for S3/Blob storage

**Fix**: Configure CORS in storage provider

**AWS S3**:
```json
{
  "AllowedHeaders": ["*"],
  "AllowedMethods": ["PUT", "POST", "GET"],
  "AllowedOrigins": ["https://yourdomain.com"],
  "ExposeHeaders": ["ETag"]
}
```

---

### Issue: Upload succeeds but image not displaying

**Cause**: File not publicly accessible

**Fix**: Set access to public or use signed URLs

**Vercel Blob**:
```typescript
await put(filename, file, {
  access: 'public' // ← Set to public
})
```

---

### Issue: Slow upload speed

**Cause**: Large uncompressed images, server routing

**Fix**: Compress images client-side before upload

```typescript
import imageCompression from 'browser-image-compression'

const compressed = await imageCompression(file, {
  maxSizeMB: 1,
  maxWidthOrHeight: 1920
})
```

---

### Issue: "Unauthorized" error

**Cause**: Not authenticated, or auth check missing

**Fix**: Ensure user is logged in, check middleware

```typescript
.middleware(async () => {
  const user = await auth()
  if (!user) throw new Error("Unauthorized") // ← Add this check
  return { userId: user.id }
})
```

---

### Issue: TypeScript error on File type

**Cause**: FormData can return `string | File`, need type guard

**Fix**: Use `instanceof File` check

```typescript
const file = formData.get('file')
if (!(file instanceof File)) {
  return { error: 'File required' }
}
// Now TypeScript knows `file` is File, not string
```

---

## Performance Optimization

### Optimize Upload Speed

1. **Client-side direct uploads** (bypass server)
   - Vercel Blob: Built-in client-side uploads
   - AWS S3: Presigned URLs

2. **Compress images before upload**
   ```typescript
   import imageCompression from 'browser-image-compression'

   const compressed = await imageCompression(file, {
     maxSizeMB: 1
   })
   ```

3. **Use edge storage**
   - Vercel Blob: Edge-native
   - UploadThing: Global CDN

---

### Optimize Storage Costs

1. **Image optimization** (30-70% size reduction)
   ```typescript
   await sharp(buffer)
     .resize(1920, 1080)
     .webp({ quality: 85 })
     .toBuffer()
   ```

2. **Choose cost-effective provider**
   - Supabase Storage: $0.021/GB (cheapest)
   - AWS S3: $0.023/GB
   - Vercel Blob: $0.05/GB

3. **Delete unused files**
   ```typescript
   // Cron job: Delete files with no database record
   const orphanedFiles = await findOrphanedFiles()
   await deleteFiles(orphanedFiles)
   ```

---

### Optimize Page Load

1. **Use CDN delivery** (all providers)
2. **Lazy load images**
   ```typescript
   <Image src={url} alt="..." loading="lazy" />
   ```

3. **Generate responsive images**
   ```typescript
   const sizes = await generateImageSizes(buffer)
   // Use srcset with thumbnail, medium, large
   ```

---

## Quick Command Reference

### UploadThing

```bash
# Install
npm install uploadthing @uploadthing/react

# Environment variables
UPLOADTHING_SECRET=sk_live_...
UPLOADTHING_APP_ID=...
```

---

### Vercel Blob

```bash
# Install
npm install @vercel/blob

# Environment variables
BLOB_READ_WRITE_TOKEN=vercel_blob_...
```

---

### Supabase Storage

```bash
# Install
npm install @supabase/supabase-js

# Environment variables
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

---

### AWS S3

```bash
# Install
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner

# Environment variables
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_BUCKET_NAME=my-app-uploads
```

---

### Image Optimization

```bash
# Install
npm install sharp

# Optional: Client-side compression
npm install browser-image-compression
```

---

### File Validation

```bash
# Install
npm install file-type

# Usage
import { fileTypeFromBuffer } from 'file-type'
const type = await fileTypeFromBuffer(buffer)
console.log(type.mime) // 'image/jpeg'
```

---

## Success Criteria

### Implementation Success

- ✅ Provider selected using decision matrix
- ✅ File upload working (single file, multi-file)
- ✅ Upload progress displayed
- ✅ File validation functioning (client + server)
- ✅ Image optimization configured (if using sharp.js)
- ✅ TypeScript types working (no `any`)

---

### Security Success

- ✅ Server-side validation active (MIME, size, magic bytes)
- ✅ Upload authorization required (authenticated users only)
- ✅ Virus scanning configured (for large files, if applicable)
- ✅ Rate limiting active (prevent spam uploads)
- ✅ Secure storage configured (RLS policies, IAM policies, presigned URLs)
- ✅ File names sanitized (prevent path traversal)

---

### Production Readiness

- ✅ Error handling (network failures, storage quota exceeded)
- ✅ Loading states (upload progress, completion)
- ✅ CDN delivery configured
- ✅ Image optimization working (30-70% size reduction)
- ✅ E2E tests passing (upload, validate, retrieve)
- ✅ Storage costs documented (monthly estimate)

---

## Additional Resources

### Documentation

- **UploadThing**: [docs.uploadthing.com](https://docs.uploadthing.com)
- **Vercel Blob**: [vercel.com/docs/storage/vercel-blob](https://vercel.com/docs/storage/vercel-blob)
- **Supabase Storage**: [supabase.com/docs/guides/storage](https://supabase.com/docs/guides/storage)
- **AWS S3**: [docs.aws.amazon.com/s3](https://docs.aws.amazon.com/s3)

### Tools

- **Sharp.js**: [sharp.pixelplumbing.com](https://sharp.pixelplumbing.com)
- **React Dropzone**: [react-dropzone.js.org](https://react-dropzone.js.org)
- **ClamAV**: [clamav.net](https://www.clamav.net)

### SAP Protocol Spec

For complete API reference, how-to guides, and tutorials, see [protocol-spec.md](protocol-spec.md)

### SAP Adoption Blueprint

For step-by-step installation guide, see [adoption-blueprint.md](adoption-blueprint.md)

---

## Version History

### 1.0.0 (2025-11-09) - Initial Release

**Added**:
- Quick reference for agents
- Upload provider decision tree
- Common workflows (4 patterns)
- Integration with SAP-033, SAP-034, SAP-041, SAP-032
- Security checklist
- 8 common pitfalls with solutions
- Troubleshooting guide
- Performance optimization
- Success criteria

**Status**: Pilot (awaiting first production adoption)

---

## Next Steps

1. **Choose Provider**: Use decision tree to select provider
2. **Read Protocol Spec**: [protocol-spec.md](protocol-spec.md) for complete API reference
3. **Follow Adoption Blueprint**: [adoption-blueprint.md](adoption-blueprint.md) for installation
4. **Test Workflows**: Implement Workflow 1 (Simple Image Uploader)
5. **Add Security**: Follow security checklist
6. **Integrate Database**: SAP-034 for file metadata
7. **Optimize**: Add image optimization with sharp.js

**Questions?** See [protocol-spec.md](protocol-spec.md) for detailed how-to guides and tutorials.
