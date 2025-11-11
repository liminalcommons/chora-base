# SAP-035: React File Upload - Adoption Blueprint

**SAP ID**: SAP-035
**Name**: react-file-upload
**Full Name**: React File Upload & Storage
**Status**: pilot
**Version**: 1.0.0
**Created**: 2025-11-09
**Last Updated**: 2025-11-09
**Diataxis Type**: How-to

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Choose Your Provider](#choose-your-provider)
3. [Option A: UploadThing (Recommended for Next.js)](#option-a-uploadthing-recommended-for-nextjs)
4. [Option B: Vercel Blob](#option-b-vercel-blob)
5. [Option C: Supabase Storage](#option-c-supabase-storage)
6. [Option D: AWS S3](#option-d-aws-s3)
7. [Optional: Add Image Optimization](#optional-add-image-optimization)
8. [Optional: Add Virus Scanning](#optional-add-virus-scanning)
9. [Validation](#validation)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

- **Next.js 15.1+** (App Router)
- **React 19+**
- **TypeScript 5.3+**
- **Authentication** (SAP-033): `auth()` function available
- **Database** (SAP-034): Prisma or Drizzle for metadata storage

### Verification

```bash
npx next --version  # Should show 15.1+
node --version      # Should show 22+
```

Verify authentication:
```typescript
// Should work:
import { auth } from "@/auth"
const user = await auth()
```

Verify database:
```typescript
// Should work:
import { prisma } from "@/lib/prisma"
// or
import { db } from "@/lib/db"
```

---

## Choose Your Provider

Use the decision matrix to select the best provider for your project:

| Provider | Best For | Setup Time | Free Tier |
|----------|----------|------------|-----------|
| **UploadThing** | Next.js apps, rapid prototyping | 15 min | ✅ 2GB storage |
| **Vercel Blob** | Vercel deployments, edge-first | 10 min | ❌ Paid only |
| **Supabase Storage** | Supabase projects, RLS | 20 min | ✅ 1GB storage |
| **AWS S3** | Enterprise, AWS infrastructure | 30 min | ✅ 5GB (12mo) |

**Decision Tree**:
```
Choose:
├─ Next.js + simple? → UploadThing
├─ Vercel + edge? → Vercel Blob
├─ Supabase + RLS? → Supabase Storage
└─ Enterprise + AWS? → AWS S3
```

**Proceed to your chosen provider's section below.**

---

## Option A: UploadThing (Recommended for Next.js)

**Time**: 15 minutes

**Best For**: Next.js applications, startups, MVPs

**What You'll Get**:
- Type-safe file router
- Pre-built UI components (`<UploadButton>`, `<UploadDropzone>`)
- Free 2GB storage
- Automatic CDN delivery

---

### Step 1: Install Dependencies (1 min)

```bash
npm install uploadthing @uploadthing/react
```

---

### Step 2: Get UploadThing API Keys (2 min)

1. Visit [uploadthing.com](https://uploadthing.com)
2. Sign up / Log in
3. Create new app
4. Copy API keys

Add to `.env.local`:
```bash
UPLOADTHING_SECRET=sk_live_...
UPLOADTHING_APP_ID=...
```

---

### Step 3: Create File Router (5 min)

Create `app/api/uploadthing/core.ts`:

```typescript
import { createUploadthing, type FileRouter } from "uploadthing/next"
import { auth } from "@/auth" // SAP-033
import { prisma } from "@/lib/prisma" // SAP-034

const f = createUploadthing()

export const ourFileRouter = {
  // Image uploader
  imageUploader: f({
    image: {
      maxFileSize: "4MB",
      maxFileCount: 4
    }
  })
    .middleware(async ({ req }) => {
      // Require authentication (SAP-033)
      const user = await auth()
      if (!user) throw new Error("Unauthorized")

      return { userId: user.id }
    })
    .onUploadComplete(async ({ metadata, file }) => {
      console.log("Upload complete for userId:", metadata.userId)
      console.log("File URL:", file.url)

      // Save to database (SAP-034)
      await prisma.upload.create({
        data: {
          url: file.url,
          key: file.key,
          name: file.name,
          size: file.size,
          type: file.type,
          userId: metadata.userId
        }
      })
    }),

  // Document uploader
  documentUploader: f({
    pdf: { maxFileSize: "16MB" },
    "application/msword": { maxFileSize: "16MB" },
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": { maxFileSize: "16MB" }
  })
    .middleware(async () => {
      const user = await auth()
      if (!user) throw new Error("Unauthorized")
      return { userId: user.id }
    })
    .onUploadComplete(async ({ metadata, file }) => {
      await prisma.upload.create({
        data: {
          url: file.url,
          userId: metadata.userId,
          type: 'document'
        }
      })
    })
} satisfies FileRouter

export type OurFileRouter = typeof ourFileRouter
```

---

### Step 4: Create API Route (2 min)

Create `app/api/uploadthing/route.ts`:

```typescript
import { createRouteHandler } from "uploadthing/next"
import { ourFileRouter } from "./core"

export const { GET, POST } = createRouteHandler({
  router: ourFileRouter
})
```

---

### Step 5: Generate UploadThing Utils (2 min)

Create `utils/uploadthing.ts`:

```typescript
import { generateReactHelpers } from "@uploadthing/react"
import type { OurFileRouter } from "@/app/api/uploadthing/core"

export const { useUploadThing, uploadFiles } =
  generateReactHelpers<OurFileRouter>()

export { UploadButton, UploadDropzone, Uploader } from "@uploadthing/react"
```

---

### Step 6: Create Upload Component (3 min)

Create `components/upload/ImageUploader.tsx`:

```typescript
"use client"

import { UploadButton } from "@/utils/uploadthing"
import { useState } from "react"
import Image from "next/image"

export function ImageUploader() {
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null)

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Upload Image</h2>

      <UploadButton
        endpoint="imageUploader"
        onClientUploadComplete={(res) => {
          console.log("Files:", res)
          if (res?.[0]) {
            setUploadedUrl(res[0].url)
          }
        }}
        onUploadError={(error: Error) => {
          alert(`ERROR! ${error.message}`)
        }}
      />

      {uploadedUrl && (
        <div className="mt-4">
          <Image
            src={uploadedUrl}
            alt="Uploaded image"
            width={400}
            height={300}
            className="rounded-lg"
          />
        </div>
      )}
    </div>
  )
}
```

---

### Step 7: Use in Page (1 min)

Create or update `app/upload/page.tsx`:

```typescript
import { ImageUploader } from "@/components/upload/ImageUploader"

export default function UploadPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Upload Files</h1>
      <ImageUploader />
    </div>
  )
}
```

---

### Step 8: Test Upload (2 min)

1. Run development server:
   ```bash
   npm run dev
   ```

2. Navigate to `/upload`

3. Click "Choose File"

4. Select an image (JPEG, PNG, WebP)

5. Verify:
   - Upload completes successfully
   - Image displays
   - Database record created (`prisma studio` or database viewer)

---

### Validation Checklist

- [ ] Upload completes successfully
- [ ] Image displays after upload
- [ ] Upload record saved to database
- [ ] Authentication required (test while logged out → should show "Unauthorized")
- [ ] File size validation works (test with >4MB file → should fail)
- [ ] File type validation works (test with .txt file → should fail)

---

**UploadThing Setup Complete!** ✅

**Next Steps**:
- Add multi-file upload (see [protocol-spec.md](protocol-spec.md#how-to-implement-multi-file-upload))
- Add image optimization (see [Optional: Add Image Optimization](#optional-add-image-optimization))
- Add virus scanning (see [Optional: Add Virus Scanning](#optional-add-virus-scanning))

---

## Option B: Vercel Blob

**Time**: 10 minutes

**Best For**: Vercel deployments, global audience, edge-first apps

**What You'll Get**:
- Edge-optimized storage
- Client-side direct uploads
- Global CDN (<50ms latency)
- Upload progress tracking

---

### Step 1: Install Dependencies (1 min)

```bash
npm install @vercel/blob
```

---

### Step 2: Get Blob Token (1 min)

**Vercel Dashboard** → Your Project → Settings → Environment Variables

Add:
```bash
BLOB_READ_WRITE_TOKEN=vercel_blob_rw_...
```

Redeploy or restart dev server for environment variable to load.

---

### Step 3: Create Upload API Route (5 min)

Create `app/api/upload/route.ts`:

```typescript
import { put } from '@vercel/blob'
import { auth } from '@/auth' // SAP-033
import { prisma } from '@/lib/prisma' // SAP-034

export async function POST(request: Request) {
  // 1. Check authentication (SAP-033)
  const session = await auth()
  if (!session) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // 2. Get file from form
  const form = await request.formData()
  const file = form.get('file') as File

  if (!file) {
    return Response.json({ error: 'No file provided' }, { status: 400 })
  }

  // 3. Validate file
  if (file.size > 4 * 1024 * 1024) {
    return Response.json({ error: 'File too large (max 4MB)' }, { status: 413 })
  }

  const validTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!validTypes.includes(file.type)) {
    return Response.json({ error: 'Invalid file type' }, { status: 400 })
  }

  // 4. Upload to Vercel Blob
  const blob = await put(file.name, file, {
    access: 'public',
    addRandomSuffix: true // Prevents filename conflicts
  })

  // 5. Save to database (SAP-034)
  await prisma.upload.create({
    data: {
      url: blob.url,
      pathname: blob.pathname,
      size: blob.size,
      userId: session.user.id
    }
  })

  return Response.json(blob)
}
```

---

### Step 4: Create Upload Component (3 min)

Create `components/upload/BlobUploader.tsx`:

```typescript
"use client"

import { useState } from "react"
import Image from "next/image"

export function BlobUploader() {
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleUpload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setIsUploading(true)
    setError(null)

    const form = e.currentTarget
    const formData = new FormData(form)

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.error || 'Upload failed')
      }

      const blob = await res.json()
      setUploadedUrl(blob.url)
    } catch (error) {
      setError((error as Error).message)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Upload Image</h2>

      <form onSubmit={handleUpload} className="mb-4">
        <input
          type="file"
          name="file"
          accept="image/*"
          required
          className="mb-2"
        />
        <button
          type="submit"
          disabled={isUploading}
          className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {isUploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>

      {error && <p className="text-red-600">{error}</p>}

      {uploadedUrl && (
        <div>
          <Image
            src={uploadedUrl}
            alt="Uploaded image"
            width={400}
            height={300}
            className="rounded-lg"
          />
        </div>
      )}
    </div>
  )
}
```

---

### Step 5: Use in Page (1 min)

Create or update `app/upload/page.tsx`:

```typescript
import { BlobUploader } from "@/components/upload/BlobUploader"

export default function UploadPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Upload Files</h1>
      <BlobUploader />
    </div>
  )
}
```

---

### Step 6: Test Upload (2 min)

1. Run: `npm run dev`
2. Navigate to `/upload`
3. Select image
4. Click "Upload"
5. Verify upload completes and image displays

---

### Validation Checklist

- [ ] Upload completes successfully
- [ ] Image displays
- [ ] Database record created
- [ ] Authentication required (test logged out)
- [ ] File size validation works (test >4MB file)
- [ ] File type validation works (test .txt file)

---

**Vercel Blob Setup Complete!** ✅

**Next Steps**:
- Add client-side direct uploads (see [protocol-spec.md](protocol-spec.md#vercel-blob-client-side-direct-upload))
- Add progress indicators
- Add image optimization

---

## Option C: Supabase Storage

**Time**: 20 minutes

**Best For**: Supabase projects, Row-Level Security, image transformations

**What You'll Get**:
- Row-Level Security (RLS)
- PostgreSQL integration
- Image transformations (resize, crop, format)
- Cost-effective ($0.021/GB)

---

### Step 1: Create Storage Bucket (3 min)

**Supabase Dashboard** → Storage → Create bucket

- **Bucket name**: `avatars` (or your preferred name)
- **Public**: ✅ YES (or use RLS for private)

Click "Create bucket"

---

### Step 2: Install Supabase Client (1 min)

```bash
npm install @supabase/supabase-js
```

Add to `.env.local`:
```bash
NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

(Get from Supabase Dashboard → Project Settings → API)

---

### Step 3: Create Supabase Client (2 min)

Create `lib/supabase.ts`:

```typescript
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

---

### Step 4: Set Up RLS Policies (5 min)

**Supabase Dashboard** → SQL Editor

Run this SQL:

```sql
-- Enable RLS on storage.objects
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Policy: Authenticated users can upload
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK (
  auth.uid() IS NOT NULL
  AND bucket_id = 'avatars'
);

-- Policy: Users can access their own files
CREATE POLICY "Users can access own files"
ON storage.objects FOR SELECT
USING (
  auth.uid() = owner
  OR bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text
);

-- Policy: Users can update their own files
CREATE POLICY "Users can update own files"
ON storage.objects FOR UPDATE
USING (auth.uid() = owner);

-- Policy: Users can delete their own files
CREATE POLICY "Users can delete own files"
ON storage.objects FOR DELETE
USING (auth.uid() = owner);
```

Click "Run"

---

### Step 5: Create Upload Component (5 min)

Create `components/upload/SupabaseUploader.tsx`:

```typescript
"use client"

import { supabase } from '@/lib/supabase'
import { useState } from 'react'
import Image from 'next/image'

export function SupabaseUploader() {
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    setError(null)

    try {
      // Get current user
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        throw new Error('Not authenticated')
      }

      // Upload file
      const filePath = `${user.id}/${Date.now()}-${file.name}`

      const { data, error: uploadError } = await supabase.storage
        .from('avatars')
        .upload(filePath, file, {
          cacheControl: '3600',
          upsert: false
        })

      if (uploadError) {
        throw uploadError
      }

      // Get public URL
      const { data: urlData } = supabase.storage
        .from('avatars')
        .getPublicUrl(data.path)

      setUploadedUrl(urlData.publicUrl)
    } catch (error) {
      setError((error as Error).message)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Upload Image</h2>

      <input
        type="file"
        accept="image/*"
        onChange={handleUpload}
        disabled={isUploading}
        className="mb-4"
      />

      {isUploading && <p>Uploading...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {uploadedUrl && (
        <div>
          <Image
            src={uploadedUrl}
            alt="Uploaded image"
            width={400}
            height={300}
            className="rounded-lg"
          />
        </div>
      )}
    </div>
  )
}
```

---

### Step 6: Use in Page (1 min)

Create or update `app/upload/page.tsx`:

```typescript
import { SupabaseUploader } from "@/components/upload/SupabaseUploader"

export default function UploadPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Upload Files</h1>
      <SupabaseUploader />
    </div>
  )
}
```

---

### Step 7: Test Upload (3 min)

1. Ensure user is authenticated (Supabase Auth)
2. Run: `npm run dev`
3. Navigate to `/upload`
4. Select image
5. Verify upload completes and image displays

---

### Validation Checklist

- [ ] Upload completes successfully
- [ ] Image displays
- [ ] RLS policies active (test logged out → should fail)
- [ ] Files stored in correct user folder
- [ ] Public URL accessible

---

**Supabase Storage Setup Complete!** ✅

**Next Steps**:
- Add image transformations (see [protocol-spec.md](protocol-spec.md#supabase-storage-image-transformations))
- Save metadata to database
- Add signed URLs for private files

---

## Option D: AWS S3

**Time**: 30 minutes

**Best For**: Enterprise applications, existing AWS infrastructure, compliance requirements

**What You'll Get**:
- 99.999999999% durability (11 nines)
- Presigned URLs for secure uploads
- Large file support (5GB max, 5TB with multipart)
- Compliance certifications (SOC2, HIPAA, PCI-DSS)

---

### Step 1: Create S3 Bucket (5 min)

**AWS Console** → S3 → Create bucket

1. **Bucket name**: `my-app-uploads` (globally unique)
2. **Region**: `us-east-1` (or your preferred region)
3. **Block public access**: ✅ ON (use presigned URLs for access)
4. Click "Create bucket"

---

### Step 2: Create IAM User (5 min)

**AWS Console** → IAM → Users → Add user

1. **Username**: `my-app-s3-uploader`
2. **Access type**: Programmatic access
3. Click "Next: Permissions"

**Attach policy**:

Click "Attach policies directly"

Click "Create policy" → JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-app-uploads/*"
    }
  ]
}
```

Name: `my-app-s3-policy`

Attach to user.

**Copy Access Key ID and Secret Access Key** (shown once!)

---

### Step 3: Configure CORS (3 min)

**S3 Bucket** → Permissions → CORS

Add:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["PUT", "POST", "GET", "DELETE"],
    "AllowedOrigins": [
      "http://localhost:3000",
      "https://yourdomain.com"
    ],
    "ExposeHeaders": ["ETag"]
  }
]
```

Save changes.

---

### Step 4: Install AWS SDK (1 min)

```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

Add to `.env.local`:

```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_BUCKET_NAME=my-app-uploads

NEXT_PUBLIC_AWS_BUCKET=my-app-uploads
NEXT_PUBLIC_AWS_REGION=us-east-1
```

---

### Step 5: Create S3 Client (2 min)

Create `lib/s3.ts`:

```typescript
import { S3Client } from "@aws-sdk/client-s3"

export const s3Client = new S3Client({
  region: process.env.AWS_REGION!,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!
  }
})
```

---

### Step 6: Create Presigned URL API (5 min)

Create `app/api/s3/presigned-url/route.ts`:

```typescript
import { s3Client } from '@/lib/s3'
import { PutObjectCommand } from "@aws-sdk/client-s3"
import { getSignedUrl } from "@aws-sdk/s3-request-presigner"
import { auth } from '@/auth' // SAP-033

export async function POST(request: Request) {
  // 1. Check authentication
  const user = await auth()
  if (!user) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // 2. Get file metadata
  const { filename, contentType } = await request.json()

  // Validate content type
  const validTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!validTypes.includes(contentType)) {
    return Response.json({ error: 'Invalid file type' }, { status: 400 })
  }

  // 3. Generate S3 key
  const key = `uploads/${user.id}/${Date.now()}-${filename}`

  // 4. Create presigned URL
  const command = new PutObjectCommand({
    Bucket: process.env.AWS_BUCKET_NAME!,
    Key: key,
    ContentType: contentType
  })

  const url = await getSignedUrl(s3Client, command, {
    expiresIn: 3600 // 1 hour
  })

  return Response.json({ url, key })
}
```

---

### Step 7: Create Upload Component (5 min)

Create `components/upload/S3Uploader.tsx`:

```typescript
"use client"

import { useState } from "react"
import Image from "next/image"

export function S3Uploader() {
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    setError(null)

    try {
      // 1. Get presigned URL from API
      const res = await fetch('/api/s3/presigned-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          contentType: file.type
        })
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.error || 'Failed to get presigned URL')
      }

      const { url, key } = await res.json()

      // 2. Upload directly to S3
      const uploadRes = await fetch(url, {
        method: 'PUT',
        body: file,
        headers: {
          'Content-Type': file.type
        }
      })

      if (!uploadRes.ok) {
        throw new Error('Failed to upload to S3')
      }

      // 3. Construct S3 URL
      const s3Url = `https://${process.env.NEXT_PUBLIC_AWS_BUCKET}.s3.${process.env.NEXT_PUBLIC_AWS_REGION}.amazonaws.com/${key}`
      setUploadedUrl(s3Url)
    } catch (error) {
      setError((error as Error).message)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Upload Image</h2>

      <input
        type="file"
        accept="image/*"
        onChange={handleUpload}
        disabled={isUploading}
        className="mb-4"
      />

      {isUploading && <p>Uploading...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {uploadedUrl && (
        <div>
          <Image
            src={uploadedUrl}
            alt="Uploaded image"
            width={400}
            height={300}
            className="rounded-lg"
          />
        </div>
      )}
    </div>
  )
}
```

---

### Step 8: Use in Page (1 min)

Create or update `app/upload/page.tsx`:

```typescript
import { S3Uploader } from "@/components/upload/S3Uploader"

export default function UploadPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Upload Files</h1>
      <S3Uploader />
    </div>
  )
}
```

---

### Step 9: Test Upload (3 min)

1. Run: `npm run dev`
2. Navigate to `/upload`
3. Select image
4. Verify upload completes
5. Check S3 bucket for uploaded file

---

### Validation Checklist

- [ ] Upload completes successfully
- [ ] Image displays
- [ ] File appears in S3 bucket
- [ ] Authentication required (test logged out)
- [ ] Presigned URL expires after 1 hour
- [ ] CORS configured correctly

---

**AWS S3 Setup Complete!** ✅

**Next Steps**:
- Add CloudFront CDN (see [protocol-spec.md](protocol-spec.md#how-to-configure-cdn-delivery))
- Add multipart upload for large files
- Save metadata to database

---

## Optional: Add Image Optimization

**Time**: 10 minutes

**Why**: Reduce file sizes by 30-70%, faster page loads, lower storage costs

---

### Step 1: Install Sharp (1 min)

```bash
npm install sharp
```

---

### Step 2: Create Optimization Function (3 min)

Create `lib/image-optimization.ts`:

```typescript
import sharp from 'sharp'

export async function optimizeImage(buffer: Buffer) {
  return await sharp(buffer)
    .rotate() // Auto-rotate based on EXIF
    .resize(1920, 1080, {
      fit: 'inside',
      withoutEnlargement: true
    })
    .webp({ quality: 85 })
    .withMetadata({
      exif: {} // Remove EXIF for privacy
    })
    .toBuffer()
}

export async function generateImageSizes(buffer: Buffer) {
  const [thumbnail, medium, large] = await Promise.all([
    sharp(buffer)
      .resize(200, 200, { fit: 'cover' })
      .webp({ quality: 80 })
      .toBuffer(),

    sharp(buffer)
      .resize(800, 600, { fit: 'inside' })
      .webp({ quality: 85 })
      .toBuffer(),

    sharp(buffer)
      .resize(1920, 1080, { fit: 'inside' })
      .webp({ quality: 90 })
      .toBuffer()
  ])

  return { thumbnail, medium, large }
}
```

---

### Step 3: Use in Upload (UploadThing Example) (5 min)

Update `app/api/uploadthing/core.ts`:

```typescript
import { optimizeImage } from '@/lib/image-optimization'

export const ourFileRouter = {
  imageUploader: f({ image: { maxFileSize: "4MB" } })
    .middleware(async () => {
      const user = await auth()
      if (!user) throw new Error("Unauthorized")
      return { userId: user.id }
    })
    .onUploadComplete(async ({ metadata, file }) => {
      // Download uploaded file
      const response = await fetch(file.url)
      const arrayBuffer = await response.arrayBuffer()
      const buffer = Buffer.from(arrayBuffer)

      // Optimize image
      const optimized = await optimizeImage(buffer)

      // Re-upload optimized version (optional: replace original)
      const optimizedUrl = await uploadToStorage(optimized, 'optimized.webp')

      // Save both URLs to database
      await prisma.upload.create({
        data: {
          url: file.url,
          optimizedUrl,
          userId: metadata.userId
        }
      })
    })
}
```

---

### Step 4: Test (1 min)

1. Upload large JPEG (e.g., 3MB)
2. Check optimized version is smaller (e.g., 1MB WebP)
3. Verify quality is acceptable

---

**Image Optimization Added!** ✅

---

## Optional: Add Virus Scanning

**Time**: 15-30 minutes (depending on provider)

**Why**: Prevent malware uploads, protect infrastructure

---

### Option 1: ClamAV Lambda (AWS S3)

**Time**: 30 minutes

**Steps**:
1. Deploy ClamAV Lambda (use [bucket-antivirus-function](https://github.com/upsidetravel/bucket-antivirus-function))
2. Configure S3 trigger on upload
3. Lambda scans file, tags as clean/infected
4. Delete infected files

---

### Option 2: Cloudflare Workers with ClamAV WASM

**Time**: 20 minutes

**Steps**:
1. Deploy Cloudflare Worker
2. Use ClamAV WASM module
3. Stream file through worker, scan before storage

---

### Option 3: Skip for Small Files (<1MB)

**Time**: 0 minutes

**Rationale**:
- For images/avatars, virus risk is low
- Focus on larger user uploads (documents, videos)

---

## Validation

### Automated Tests

Create `tests/upload.test.ts`:

```typescript
import { describe, it, expect } from 'vitest'

describe('File Upload', () => {
  it('should upload image successfully', async () => {
    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
    const formData = new FormData()
    formData.append('file', file)

    const res = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    })

    expect(res.ok).toBe(true)
  })

  it('should reject file >4MB', async () => {
    const largeFile = new File([new ArrayBuffer(5 * 1024 * 1024)], 'large.jpg', { type: 'image/jpeg' })
    const formData = new FormData()
    formData.append('file', largeFile)

    const res = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    })

    expect(res.status).toBe(413)
  })

  it('should reject invalid file type', async () => {
    const file = new File(['test'], 'test.txt', { type: 'text/plain' })
    const formData = new FormData()
    formData.append('file', file)

    const res = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    })

    expect(res.status).toBe(400)
  })
})
```

Run:
```bash
npm run test
```

---

### Manual Testing

**Test Cases**:

1. **Happy Path**:
   - [ ] Upload valid image (JPEG, PNG, WebP)
   - [ ] Verify image displays
   - [ ] Verify database record created

2. **Authentication**:
   - [ ] Try upload while logged out → Should fail with "Unauthorized"

3. **File Size Validation**:
   - [ ] Upload file >4MB → Should fail with "File too large"

4. **File Type Validation**:
   - [ ] Upload .txt file → Should fail with "Invalid file type"
   - [ ] Upload .exe file → Should fail

5. **Multi-File Upload** (if implemented):
   - [ ] Upload 3 images → All should upload
   - [ ] Verify all images display

6. **Progress Indicators** (if implemented):
   - [ ] Upload large file (2-3MB)
   - [ ] Verify progress bar updates

---

## Troubleshooting

### Issue: "CORS error" when uploading

**Cause**: Missing CORS configuration

**Fix**:

**AWS S3**: Add CORS policy (see Step 3 in [Option D: AWS S3](#step-3-configure-cors-3-min))

**Vercel Blob**: No CORS needed (edge-native)

**Supabase**: CORS configured by default

---

### Issue: "Unauthorized" error

**Cause**: User not authenticated, or auth check missing

**Fix**:

1. Verify user is logged in (SAP-033)
2. Check middleware:
   ```typescript
   .middleware(async () => {
     const user = await auth()
     if (!user) throw new Error("Unauthorized") // ← Ensure this exists
     return { userId: user.id }
   })
   ```

---

### Issue: Upload succeeds but image not displaying

**Cause**: File not publicly accessible

**Fix**:

**Vercel Blob**: Set `access: 'public'`
```typescript
await put(filename, file, {
  access: 'public' // ← Add this
})
```

**Supabase**: Use public bucket or signed URLs

**AWS S3**: Use presigned URLs for private buckets

---

### Issue: "File too large" error for small files

**Cause**: Body size limit in Next.js

**Fix**:

Add to `next.config.js`:
```javascript
module.exports = {
  api: {
    bodyParser: {
      sizeLimit: '10mb' // Increase from default 1mb
    }
  }
}
```

---

### Issue: TypeScript error "Type 'string | File' is not assignable to type 'File'"

**Cause**: FormData can return `string | File`

**Fix**: Use type guard
```typescript
const file = formData.get('file')
if (!(file instanceof File)) {
  return { error: 'File required' }
}
// Now TypeScript knows `file` is File
```

---

## Next Steps

### Production Checklist

- [ ] Provider selected and configured
- [ ] File uploads working (single + multi)
- [ ] Authentication required
- [ ] File validation (client + server)
- [ ] Image optimization (if applicable)
- [ ] Virus scanning (if applicable)
- [ ] Database integration (SAP-034)
- [ ] CDN delivery configured
- [ ] Error handling implemented
- [ ] Tests passing
- [ ] Storage costs documented

---

### Advanced Features

1. **Add drag-and-drop** (see [protocol-spec.md](protocol-spec.md#how-to-add-drag-and-drop-upload))
2. **Add image cropping** (see Tutorial 3 in [protocol-spec.md](protocol-spec.md#tutorial-3-avatar-uploader-with-crop))
3. **Add resumable uploads** (for large files >100MB)
4. **Add file management dashboard** (view, delete, search uploaded files)

---

## Support

**Documentation**:
- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete API reference
- **Awareness Guide**: [awareness-guide.md](awareness-guide.md) - Quick reference for agents

**Provider Docs**:
- **UploadThing**: [docs.uploadthing.com](https://docs.uploadthing.com)
- **Vercel Blob**: [vercel.com/docs/storage/vercel-blob](https://vercel.com/docs/storage/vercel-blob)
- **Supabase Storage**: [supabase.com/docs/guides/storage](https://supabase.com/docs/guides/storage)
- **AWS S3**: [docs.aws.amazon.com/s3](https://docs.aws.amazon.com/s3)

---

## Version History

### 1.0.0 (2025-11-09) - Initial Release

**Added**:
- Complete installation guide for 4 providers (UploadThing, Vercel Blob, Supabase Storage, AWS S3)
- Step-by-step setup (15-30 minutes per provider)
- Optional image optimization guide
- Optional virus scanning guide
- Validation checklist
- Troubleshooting guide

**Status**: Pilot (awaiting first production adoption)

---

**Adoption Complete!** 🎉

You now have production-ready file uploads with security, validation, and optimization.

**Next**: Read [protocol-spec.md](protocol-spec.md) for advanced patterns and tutorials.
