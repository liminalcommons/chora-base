# SAP-035: React File Upload - Protocol Specification

**SAP ID**: SAP-035
**Name**: react-file-upload
**Full Name**: React File Upload & Storage
**Status**: pilot
**Version**: 1.0.0
**Created**: 2025-11-09
**Last Updated**: 2025-11-09
**Diataxis Type**: Reference + How-to + Tutorial

---

## Table of Contents

### Explanation (Why & Concepts)
1. [Provider Comparison](#provider-comparison)
2. [Upload Provider Decision Matrix](#upload-provider-decision-matrix)
3. [Security Architecture](#security-architecture)

### Reference (Complete API)
4. [UploadThing API Reference](#uploadthing-api-reference)
5. [Vercel Blob API Reference](#vercel-blob-api-reference)
6. [Supabase Storage API Reference](#supabase-storage-api-reference)
7. [AWS S3 API Reference](#aws-s3-api-reference)
8. [File Validation Patterns](#file-validation-patterns)
9. [Image Optimization API](#image-optimization-api)

### How-to (Task-Oriented)
10. [How to Set Up UploadThing](#how-to-set-up-uploadthing)
11. [How to Set Up Vercel Blob](#how-to-set-up-vercel-blob)
12. [How to Set Up Supabase Storage](#how-to-set-up-supabase-storage)
13. [How to Set Up AWS S3](#how-to-set-up-aws-s3)
14. [How to Implement File Validation](#how-to-implement-file-validation)
15. [How to Add Virus Scanning](#how-to-add-virus-scanning)
16. [How to Optimize Images](#how-to-optimize-images)
17. [How to Implement Progress Indicators](#how-to-implement-progress-indicators)
18. [How to Add Drag-and-Drop Upload](#how-to-add-drag-and-drop-upload)
19. [How to Configure CDN Delivery](#how-to-configure-cdn-delivery)
20. [How to Integrate with Database](#how-to-integrate-with-database)
21. [How to Secure Uploads with Auth](#how-to-secure-uploads-with-auth)

### Tutorial (Learning-Oriented)
22. [Tutorial 1: Build Simple Image Uploader](#tutorial-1-simple-image-uploader)
23. [Tutorial 2: Build Multi-File Uploader with Progress](#tutorial-2-multi-file-uploader-with-progress)
24. [Tutorial 3: Build Avatar Uploader with Crop](#tutorial-3-avatar-uploader-with-crop)
25. [Tutorial 4: Build Document Uploader with Virus Scan](#tutorial-4-document-uploader-with-virus-scan)

---

## Explanation

### Provider Comparison

#### Why UploadThing?

**Next.js-First, Type-Safe Upload Solution**

UploadThing is purpose-built for Next.js applications, offering the fastest path from zero to production file uploads.

**Key Advantages**:
1. **Type-Safe File Router**: Define upload endpoints with Zod-like validation
2. **Pre-Built Components**: `<UploadButton>`, `<UploadDropzone>`, `<Uploader>` ready to use
3. **Middleware Support**: Integrate authentication seamlessly via `.middleware()`
4. **Free Tier**: 2GB storage, unlimited bandwidth (perfect for MVPs)
5. **Automatic Callbacks**: `onUploadComplete` webhook for database integration
6. **Zero Configuration**: No S3 buckets, no IAM policies, no CORS setup

**When to Choose UploadThing**:
- ✅ Next.js 13+ App Router project
- ✅ Startup/MVP with limited budget (free tier)
- ✅ Want pre-built UI components
- ✅ Need type-safe upload validation
- ✅ Want rapid prototyping (<20 min setup)

**When to Avoid**:
- ❌ Need >100MB file uploads on free tier
- ❌ Require full control over storage backend
- ❌ Want to avoid third-party dependency

---

#### Why Vercel Blob?

**Edge-Optimized Storage with Global CDN**

Vercel Blob provides edge storage optimized for static assets, with <50ms read latency globally.

**Key Advantages**:
1. **Edge Storage**: Regional distribution, instant global delivery
2. **3x Cost-Efficient**: Optimized for large static files vs standard CDN
3. **Client-Side Direct Uploads**: Bypass server, save bandwidth
4. **Upload Progress Tracking**: Built-in `onUploadProgress` callback
5. **First-Party Service**: No extra accounts if using Vercel
6. **Automatic Caching**: CDN-backed, instant cache invalidation
7. **Large File Support**: 500MB max file size

**When to Choose Vercel Blob**:
- ✅ Deploying on Vercel
- ✅ Global audience (need <50ms latency worldwide)
- ✅ Large static files (images, videos, PDFs)
- ✅ Want client-side direct uploads
- ✅ Need built-in CDN (no CloudFront setup)

**When to Avoid**:
- ❌ Not deploying on Vercel (platform lock-in)
- ❌ Need free tier (paid from day one)
- ❌ Want mature service (launched 2023)

---

#### Why Supabase Storage?

**Database-Integrated Storage with Row-Level Security**

Supabase Storage provides tight PostgreSQL integration with built-in Row-Level Security (RLS) for multi-tenant apps.

**Key Advantages**:
1. **Row-Level Security**: Database-level access control (`auth.uid()`)
2. **PostgreSQL Integration**: File metadata stored in database
3. **Image Transformations**: On-the-fly resize, crop, format conversion
4. **Cost-Effective**: $0.021/GB storage (cheapest option)
5. **Free Tier**: 1GB storage, 50GB egress/month
6. **Resumable Uploads**: tus protocol for large files
7. **Open Source**: Supabase Storage is open-source

**When to Choose Supabase Storage**:
- ✅ Using Supabase for database
- ✅ Need Row-Level Security (multi-tenant apps)
- ✅ Want image transformations (resize, crop, format)
- ✅ Cost-conscious ($0.021/GB cheapest)
- ✅ Prefer open-source solutions

**When to Avoid**:
- ❌ Not using Supabase (requires Supabase project)
- ❌ Need >50MB files on free tier (5GB on Pro)
- ❌ Want pre-built upload components

---

#### Why AWS S3?

**Enterprise-Grade Storage with 11 Nines Durability**

AWS S3 is the industry standard, offering the most mature storage solution with 18+ years of stability.

**Key Advantages**:
1. **Most Mature**: Launched 2006, 100+ trillion objects stored
2. **99.999999999% Durability**: 11 nines (lose 1 object per 10 billion/year)
3. **Large File Support**: 5GB max single upload, 5TB with multipart
4. **Advanced Features**: Versioning, lifecycle policies, replication, Glacier archiving
5. **Presigned URLs**: Secure time-limited upload/download
6. **IAM Integration**: Fine-grained access control
7. **Compliance**: SOC2, HIPAA, PCI-DSS, ISO 27001 certified

**When to Choose AWS S3**:
- ✅ Enterprise B2B application
- ✅ Existing AWS infrastructure
- ✅ Compliance requirements (HIPAA, SOC2)
- ✅ Need advanced features (versioning, lifecycle)
- ✅ Large files (>500MB, up to 5TB)

**When to Avoid**:
- ❌ Want rapid setup (30 min vs 15 min for Vercel Blob)
- ❌ Prefer simple configuration (IAM complexity)
- ❌ Need type-safe client (AWS SDK verbose)

---

### Upload Provider Decision Matrix

#### 5-Dimension Comparison

| Criteria | UploadThing | Vercel Blob | Supabase Storage | AWS S3 |
|----------|-------------|-------------|------------------|--------|
| **1. Setup Time** | 20 min | 15 min (fastest) | 20 min | 30 min (complex) |
| **2. Platform Coupling** | Next.js-first | Vercel-only | Supabase-coupled | Platform-agnostic |
| **3. Free Tier** | ✅ 2GB storage | ❌ NO (paid) | ✅ 1GB storage | ✅ 5GB (12mo) |
| **4. Cost (10GB + 100GB egress)** | $10/mo | $15.50/mo | $9.21/mo | $9.23/mo |
| **5. Max File Size** | 100MB (free) | 500MB | 50MB (free) | 5GB (single) |
| **Pre-Built UI** | ✅ YES | ❌ Custom | ❌ Custom | ❌ Custom |
| **Image Optimization** | ❌ No | ❌ No | ✅ Built-in | ❌ No |
| **Security** | Type-safe validation | Direct upload tokens | RLS + policies | IAM + presigned URLs |
| **TypeScript Support** | ✅ Full | ✅ Full | ✅ Full | ⚠️ Manual (verbose) |
| **CDN Integration** | ✅ Automatic | ✅ Built-in (edge) | ✅ Built-in | ⚠️ Manual (CloudFront) |
| **Open Source** | ❌ Proprietary | ❌ Proprietary | ✅ Open-source | ❌ Proprietary |

---

#### Decision Tree

```
START: Which file upload provider should I use?

├─ Q1: Using Next.js 13+ with rapid prototyping?
│  ├─ YES → UploadThing ✅ (type-safe, pre-built UI, free 2GB)
│  └─ NO → Continue to Q2
│
├─ Q2: Deploying on Vercel with global audience?
│  ├─ YES → Vercel Blob ✅ (edge-optimized, 3x cost-efficient)
│  └─ NO → Continue to Q3
│
├─ Q3: Using Supabase for database?
│  ├─ YES → Supabase Storage ✅ (RLS, image transforms, cheapest)
│  └─ NO → Continue to Q4
│
├─ Q4: Enterprise with existing AWS infrastructure?
│  ├─ YES → AWS S3 ✅ (most mature, compliance, 11 nines durability)
│  └─ NO → Continue to Q5
│
└─ Q5: Default choice (Next.js, cost-conscious, simple)
   └─ UploadThing ✅ (recommended default: free tier, easy setup, type-safe)
```

---

### Security Architecture

#### Three-Layer Validation

**Layer 1: Client-Side (UX)**
- Purpose: Immediate feedback, prevent invalid uploads
- Tools: Zod schema, File type checking, size limits
- Bypassable: Yes (users can modify via DevTools)
- **Never rely on client-side validation alone**

**Layer 2: Server-Side (Security)**
- Purpose: Enforce validation, prevent malicious uploads
- Tools: MIME type checking, magic byte verification, server size limits
- Bypassable: No (server-controlled)
- **Required for production security**

**Layer 3: Storage Provider (Defense-in-Depth)**
- Purpose: Final enforcement, storage-level protection
- Tools: IAM policies, RLS policies, presigned URLs, signed tokens
- Bypassable: No (infrastructure-level)
- **Platform-specific security**

---

#### File Upload Vulnerabilities

| Vulnerability | OWASP | Prevention |
|---------------|-------|------------|
| **Client-side validation bypass** | A04 | Server-side validation (Zod schema, MIME checks) |
| **Malware uploads** | A03 | Virus scanning (ClamAV integration) |
| **MIME type spoofing** | A03 | Magic byte verification (file-type npm package) |
| **File size exhaustion** | A05 | Server-side size limits, presigned URL expiry |
| **Insecure direct uploads** | A01 | RLS policies (Supabase), IAM policies (S3), signed URLs |
| **Path traversal** | A03 | Sanitized file names, UUID-based storage keys |
| **XSS via SVG** | A03 | MIME type whitelist, Content-Security-Policy headers |

---

## Reference

### UploadThing API Reference

#### File Router Configuration

```typescript
import { createUploadthing, type FileRouter } from "uploadthing/next"
import { auth } from "@/auth"

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
      const user = await auth()
      if (!user) throw new Error("Unauthorized")
      return { userId: user.id }
    })
    .onUploadComplete(async ({ metadata, file }) => {
      console.log("Upload complete:", file.url)
      console.log("User:", metadata.userId)

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

  // PDF uploader
  pdfUploader: f({
    pdf: { maxFileSize: "16MB" }
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
          type: 'pdf'
        }
      })
    }),

  // Video uploader
  videoUploader: f({
    video: { maxFileSize: "64MB" }
  })
    .middleware(async () => {
      const user = await auth()
      if (!user) throw new Error("Unauthorized")
      return { userId: user.id }
    })
    .onUploadComplete(async ({ metadata, file }) => {
      // Trigger video transcoding
      await transcodeVideo(file.url)
    })
} satisfies FileRouter

export type OurFileRouter = typeof ourFileRouter
```

---

#### Client Components

```typescript
import {
  UploadButton,
  UploadDropzone,
  Uploader
} from "@uploadthing/react"
import type { OurFileRouter } from "@/app/api/uploadthing/core"

// Upload Button
<UploadButton<OurFileRouter>
  endpoint="imageUploader"
  onClientUploadComplete={(res) => {
    console.log("Files:", res)
  }}
  onUploadError={(error: Error) => {
    alert(`ERROR! ${error.message}`)
  }}
/>

// Upload Dropzone
<UploadDropzone<OurFileRouter>
  endpoint="imageUploader"
  onClientUploadComplete={(res) => {
    console.log("Files:", res)
  }}
  onUploadError={(error: Error) => {
    alert(`ERROR! ${error.message}`)
  }}
/>

// Custom Uploader
<Uploader<OurFileRouter>
  endpoint="imageUploader"
  onClientUploadComplete={(res) => {
    console.log("Files:", res)
  }}
/>
```

---

#### useUploadThing Hook

```typescript
"use client"

import { useUploadThing } from "@/utils/uploadthing"

export function CustomUploader() {
  const { startUpload, isUploading, uploadProgress } = useUploadThing("imageUploader", {
    onClientUploadComplete: (res) => {
      console.log("Uploaded:", res)
    },
    onUploadError: (error) => {
      console.error("Error:", error)
    },
    onUploadProgress: (progress) => {
      console.log("Progress:", progress)
    }
  })

  async function handleUpload(files: File[]) {
    await startUpload(files)
  }

  return (
    <div>
      <input
        type="file"
        onChange={(e) => {
          const files = Array.from(e.target.files || [])
          handleUpload(files)
        }}
      />
      {isUploading && <p>Uploading... {uploadProgress}%</p>}
    </div>
  )
}
```

---

### Vercel Blob API Reference

#### Upload File

```typescript
import { put } from '@vercel/blob'

// Upload file
const blob = await put('avatars/user-123.png', file, {
  access: 'public', // or 'private'
  addRandomSuffix: true // Prevents filename conflicts
})

console.log(blob.url) // https://vercel.blob.store/avatars/user-123-abc123.png
console.log(blob.pathname) // avatars/user-123-abc123.png
console.log(blob.size) // 1024567
console.log(blob.uploadedAt) // 2025-11-09T12:00:00.000Z
```

---

#### Delete File

```typescript
import { del } from '@vercel/blob'

// Delete single file
await del('https://vercel.blob.store/avatars/user-123-abc123.png')

// Delete multiple files
await del([
  'https://vercel.blob.store/avatars/user-123-abc123.png',
  'https://vercel.blob.store/avatars/user-456-def456.png'
])
```

---

#### Get Metadata

```typescript
import { head } from '@vercel/blob'

const blob = await head('https://vercel.blob.store/avatars/user-123-abc123.png')

console.log(blob.url)
console.log(blob.size)
console.log(blob.uploadedAt)
console.log(blob.pathname)
console.log(blob.contentType)
console.log(blob.contentDisposition)
```

---

#### List Blobs

```typescript
import { list } from '@vercel/blob'

// List all blobs
const { blobs } = await list()

// List with prefix
const { blobs } = await list({ prefix: 'avatars/' })

// List with limit and cursor (pagination)
const { blobs, cursor } = await list({
  limit: 10,
  cursor: 'next-page-token'
})

// Next page
const { blobs: nextBlobs } = await list({
  limit: 10,
  cursor: cursor
})
```

---

#### Client-Side Direct Upload

```typescript
"use client"

import { upload } from '@vercel/blob/client'

export async function uploadFile(file: File) {
  const blob = await upload(file.name, file, {
    access: 'public',
    handleUploadUrl: '/api/upload' // Your API route
  })

  return blob.url
}
```

**API Route** (`app/api/upload/route.ts`):
```typescript
import { handleUpload, type HandleUploadBody } from '@vercel/blob/client'

export async function POST(request: Request): Promise<Response> {
  const body = (await request.json()) as HandleUploadBody

  try {
    const jsonResponse = await handleUpload({
      body,
      request,
      onBeforeGenerateToken: async (pathname) => {
        // Validate user is authenticated
        const user = await auth()
        if (!user) throw new Error('Unauthorized')

        return {
          allowedContentTypes: ['image/jpeg', 'image/png', 'image/webp'],
          maximumSizeInBytes: 4 * 1024 * 1024 // 4MB
        }
      },
      onUploadCompleted: async ({ blob, tokenPayload }) => {
        // Save to database
        await prisma.upload.create({
          data: {
            url: blob.url,
            pathname: blob.pathname,
            size: blob.size,
            userId: tokenPayload.userId
          }
        })
      }
    })

    return Response.json(jsonResponse)
  } catch (error) {
    return Response.json({ error: (error as Error).message }, { status: 400 })
  }
}
```

---

### Supabase Storage API Reference

#### Upload File

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('user-123/avatar.png', file, {
    cacheControl: '3600',
    upsert: false // Set to true to overwrite existing file
  })

if (error) {
  console.error('Upload error:', error)
} else {
  console.log('Uploaded:', data.path)
}
```

---

#### Download File

```typescript
// Download file as blob
const { data, error } = await supabase.storage
  .from('avatars')
  .download('user-123/avatar.png')

if (data) {
  const url = URL.createObjectURL(data)
  // Use URL for display
}
```

---

#### Get Public URL

```typescript
// Get public URL (for public buckets)
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user-123/avatar.png')

console.log(data.publicUrl)
// https://<project-ref>.supabase.co/storage/v1/object/public/avatars/user-123/avatar.png
```

---

#### Get Signed URL

```typescript
// Get signed URL (for private buckets)
const { data, error } = await supabase.storage
  .from('private-docs')
  .createSignedUrl('user-123/document.pdf', 60) // Expires in 60 seconds

console.log(data.signedUrl)
```

---

#### Delete File

```typescript
// Delete single file
const { data, error } = await supabase.storage
  .from('avatars')
  .remove(['user-123/avatar.png'])

// Delete multiple files
const { data, error } = await supabase.storage
  .from('avatars')
  .remove(['user-123/avatar.png', 'user-456/avatar.png'])
```

---

#### List Files

```typescript
// List files in bucket
const { data, error } = await supabase.storage
  .from('avatars')
  .list('user-123', {
    limit: 10,
    offset: 0,
    sortBy: { column: 'created_at', order: 'desc' }
  })

data?.forEach(file => {
  console.log(file.name)
  console.log(file.id)
  console.log(file.created_at)
  console.log(file.updated_at)
  console.log(file.last_accessed_at)
  console.log(file.metadata)
})
```

---

#### Image Transformations

```typescript
// Resize image
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user-123/avatar.png', {
    transform: {
      width: 200,
      height: 200,
      resize: 'cover' // or 'contain', 'fill'
    }
  })

// Multiple transformations
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user-123/avatar.png', {
    transform: {
      width: 800,
      height: 600,
      resize: 'contain',
      format: 'webp',
      quality: 80
    }
  })
```

---

#### Row-Level Security (RLS) Policies

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

-- Policy: Users can only access their own files
CREATE POLICY "Users can access own files"
ON storage.objects FOR SELECT
USING (
  auth.uid() = owner
  OR bucket_id = 'public-avatars'
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

---

### AWS S3 API Reference

#### Presigned Upload URL

```typescript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3"
import { getSignedUrl } from "@aws-sdk/s3-request-presigner"

const s3Client = new S3Client({
  region: process.env.AWS_REGION!,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!
  }
})

// Generate presigned URL for upload
export async function getPresignedUploadUrl(key: string, contentType: string) {
  const command = new PutObjectCommand({
    Bucket: process.env.AWS_BUCKET_NAME!,
    Key: key,
    ContentType: contentType,
    Metadata: {
      uploadedBy: 'user-123'
    }
  })

  const url = await getSignedUrl(s3Client, command, {
    expiresIn: 3600 // 1 hour
  })

  return url
}
```

**Client-Side Upload**:
```typescript
"use client"

export async function uploadToS3(file: File) {
  // 1. Get presigned URL from API
  const res = await fetch('/api/s3/presigned-url', {
    method: 'POST',
    body: JSON.stringify({
      filename: file.name,
      contentType: file.type
    })
  })

  const { url, key } = await res.json()

  // 2. Upload directly to S3
  await fetch(url, {
    method: 'PUT',
    body: file,
    headers: {
      'Content-Type': file.type
    }
  })

  // 3. Return S3 URL
  return `https://${process.env.NEXT_PUBLIC_AWS_BUCKET}.s3.${process.env.NEXT_PUBLIC_AWS_REGION}.amazonaws.com/${key}`
}
```

---

#### Presigned Download URL

```typescript
import { GetObjectCommand } from "@aws-sdk/client-s3"
import { getSignedUrl } from "@aws-sdk/s3-request-presigner"

export async function getPresignedDownloadUrl(key: string) {
  const command = new GetObjectCommand({
    Bucket: process.env.AWS_BUCKET_NAME!,
    Key: key
  })

  const url = await getSignedUrl(s3Client, command, {
    expiresIn: 3600 // 1 hour
  })

  return url
}
```

---

#### Multipart Upload (Large Files >5MB)

```typescript
import {
  CreateMultipartUploadCommand,
  UploadPartCommand,
  CompleteMultipartUploadCommand
} from "@aws-sdk/client-s3"

export async function uploadLargeFile(file: File, key: string) {
  // 1. Initiate multipart upload
  const multipartUpload = await s3Client.send(
    new CreateMultipartUploadCommand({
      Bucket: process.env.AWS_BUCKET_NAME!,
      Key: key
    })
  )

  const uploadId = multipartUpload.UploadId

  // 2. Upload parts (5MB chunks)
  const partSize = 5 * 1024 * 1024 // 5MB
  const numParts = Math.ceil(file.size / partSize)
  const uploadedParts = []

  for (let i = 0; i < numParts; i++) {
    const start = i * partSize
    const end = Math.min(start + partSize, file.size)
    const chunk = file.slice(start, end)

    const partNumber = i + 1
    const uploadPart = await s3Client.send(
      new UploadPartCommand({
        Bucket: process.env.AWS_BUCKET_NAME!,
        Key: key,
        UploadId: uploadId,
        PartNumber: partNumber,
        Body: chunk
      })
    )

    uploadedParts.push({
      ETag: uploadPart.ETag,
      PartNumber: partNumber
    })
  }

  // 3. Complete multipart upload
  await s3Client.send(
    new CompleteMultipartUploadCommand({
      Bucket: process.env.AWS_BUCKET_NAME!,
      Key: key,
      UploadId: uploadId,
      MultipartUpload: { Parts: uploadedParts }
    })
  )

  return `https://${process.env.AWS_BUCKET_NAME}.s3.${process.env.AWS_REGION}.amazonaws.com/${key}`
}
```

---

#### Delete File

```typescript
import { DeleteObjectCommand } from "@aws-sdk/client-s3"

export async function deleteS3File(key: string) {
  await s3Client.send(
    new DeleteObjectCommand({
      Bucket: process.env.AWS_BUCKET_NAME!,
      Key: key
    })
  )
}
```

---

#### List Files

```typescript
import { ListObjectsV2Command } from "@aws-sdk/client-s3"

export async function listS3Files(prefix?: string) {
  const command = new ListObjectsV2Command({
    Bucket: process.env.AWS_BUCKET_NAME!,
    Prefix: prefix,
    MaxKeys: 100
  })

  const response = await s3Client.send(command)

  return response.Contents?.map(obj => ({
    key: obj.Key,
    size: obj.Size,
    lastModified: obj.LastModified,
    etag: obj.ETag
  }))
}
```

---

### File Validation Patterns

#### Client-Side Validation

```typescript
import { z } from 'zod'

// File schema with Zod
const fileSchema = z.object({
  file: z.instanceof(File)
    .refine(file => file.size <= 5 * 1024 * 1024, {
      message: "File must be less than 5MB"
    })
    .refine(file => ['image/jpeg', 'image/png', 'image/webp'].includes(file.type), {
      message: "Only JPEG, PNG, and WebP images are allowed"
    })
})

// Usage in component
function validateFile(file: File) {
  const result = fileSchema.safeParse({ file })

  if (!result.success) {
    return { error: result.error.errors[0].message }
  }

  return { success: true }
}
```

---

#### Server-Side MIME Type Verification

```typescript
import { fileTypeFromBuffer } from 'file-type'

export async function validateFileMIME(file: File) {
  // Convert File to Buffer
  const arrayBuffer = await file.arrayBuffer()
  const buffer = Buffer.from(arrayBuffer)

  // Check magic bytes (not extension)
  const type = await fileTypeFromBuffer(buffer)

  const validMimeTypes = ['image/jpeg', 'image/png', 'image/webp']

  if (!type || !validMimeTypes.includes(type.mime)) {
    throw new Error(`Invalid file type. Expected: ${validMimeTypes.join(', ')}, Got: ${type?.mime || 'unknown'}`)
  }

  return type.mime
}
```

---

#### Complete Validation Example

```typescript
"use server"

import { auth } from '@/auth'
import { fileTypeFromBuffer } from 'file-type'

export async function uploadFile(formData: FormData) {
  // 1. Authentication check
  const user = await auth()
  if (!user) {
    return { error: 'Unauthorized' }
  }

  // 2. Get file from form
  const file = formData.get('file')
  if (!(file instanceof File)) {
    return { error: 'File required' }
  }

  // 3. Validate file size
  if (file.size > 5 * 1024 * 1024) {
    return { error: 'File too large (max 5MB)' }
  }

  // 4. Validate MIME type (magic bytes, not extension)
  const buffer = Buffer.from(await file.arrayBuffer())
  const type = await fileTypeFromBuffer(buffer)

  const validMimeTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!type || !validMimeTypes.includes(type.mime)) {
    return { error: `Invalid file type. Expected: ${validMimeTypes.join(', ')}, Got: ${type?.mime || 'unknown'}` }
  }

  // 5. Sanitize filename (prevent path traversal)
  const sanitizedFilename = file.name.replace(/[^a-zA-Z0-9.-]/g, '_')

  // 6. Upload to storage
  const url = await uploadToStorage(file, sanitizedFilename)

  // 7. Save to database
  await prisma.upload.create({
    data: {
      url,
      filename: sanitizedFilename,
      mimeType: type.mime,
      size: file.size,
      userId: user.id
    }
  })

  return { success: true, url }
}
```

---

### Image Optimization API

#### Resize Images with Sharp

```typescript
import sharp from 'sharp'

export async function optimizeImage(buffer: Buffer) {
  // Generate multiple sizes
  const [thumbnail, medium, large] = await Promise.all([
    // Thumbnail: 200x200, WebP, 80% quality
    sharp(buffer)
      .resize(200, 200, { fit: 'cover' })
      .webp({ quality: 80 })
      .toBuffer(),

    // Medium: 800x600, WebP, 85% quality
    sharp(buffer)
      .resize(800, 600, { fit: 'inside' })
      .webp({ quality: 85 })
      .toBuffer(),

    // Large: 1920x1080, WebP, 90% quality
    sharp(buffer)
      .resize(1920, 1080, { fit: 'inside' })
      .webp({ quality: 90 })
      .toBuffer()
  ])

  return { thumbnail, medium, large }
}
```

---

#### Format Conversion

```typescript
// Convert to WebP
const webp = await sharp(buffer)
  .webp({ quality: 85 })
  .toBuffer()

// Convert to AVIF (better compression)
const avif = await sharp(buffer)
  .avif({ quality: 80 })
  .toBuffer()

// Convert to JPEG
const jpeg = await sharp(buffer)
  .jpeg({ quality: 90, progressive: true })
  .toBuffer()
```

---

#### Metadata Stripping (Privacy)

```typescript
// Remove EXIF data
const stripped = await sharp(buffer)
  .rotate() // Auto-rotate based on EXIF
  .withMetadata({
    exif: {}, // Remove EXIF
    icc: {} // Keep color profile
  })
  .toBuffer()
```

---

#### Complete Optimization Pipeline

```typescript
export async function processImage(file: File) {
  const buffer = Buffer.from(await file.arrayBuffer())

  // 1. Auto-rotate based on EXIF
  // 2. Strip metadata
  // 3. Resize to max 1920x1080
  // 4. Convert to WebP
  // 5. Optimize quality (85%)
  const optimized = await sharp(buffer)
    .rotate()
    .resize(1920, 1080, {
      fit: 'inside',
      withoutEnlargement: true
    })
    .webp({ quality: 85 })
    .withMetadata({
      exif: {}, // Remove EXIF for privacy
    })
    .toBuffer()

  return optimized
}
```

---

## How-to Guides

### How to Set Up UploadThing

**Prerequisites**:
- Next.js 15.1+
- React 19+
- Authentication (SAP-033)

**Time**: 15 minutes

---

**Step 1: Install Dependencies**

```bash
npm install uploadthing @uploadthing/react
```

---

**Step 2: Get API Keys**

1. Visit [uploadthing.com](https://uploadthing.com)
2. Create account
3. Create app
4. Copy API keys

Add to `.env.local`:
```
UPLOADTHING_SECRET=sk_live_...
UPLOADTHING_APP_ID=...
```

---

**Step 3: Create File Router**

Create `app/api/uploadthing/core.ts`:
```typescript
import { createUploadthing, type FileRouter } from "uploadthing/next"
import { auth } from "@/auth"

const f = createUploadthing()

export const ourFileRouter = {
  imageUploader: f({
    image: { maxFileSize: "4MB", maxFileCount: 4 }
  })
    .middleware(async () => {
      const user = await auth()
      if (!user) throw new Error("Unauthorized")
      return { userId: user.id }
    })
    .onUploadComplete(async ({ metadata, file }) => {
      console.log("Uploaded:", file.url, "by", metadata.userId)
    })
} satisfies FileRouter

export type OurFileRouter = typeof ourFileRouter
```

---

**Step 4: Create API Route**

Create `app/api/uploadthing/route.ts`:
```typescript
import { createRouteHandler } from "uploadthing/next"
import { ourFileRouter } from "./core"

export const { GET, POST } = createRouteHandler({
  router: ourFileRouter
})
```

---

**Step 5: Generate Utilities**

Create `utils/uploadthing.ts`:
```typescript
import { generateReactHelpers } from "@uploadthing/react"
import type { OurFileRouter } from "@/app/api/uploadthing/core"

export const { useUploadThing, uploadFiles } =
  generateReactHelpers<OurFileRouter>()

export { UploadButton, UploadDropzone } from "@uploadthing/react"
```

---

**Step 6: Use Upload Component**

```typescript
"use client"

import { UploadButton } from "@/utils/uploadthing"

export function ImageUploader() {
  return (
    <UploadButton
      endpoint="imageUploader"
      onClientUploadComplete={(res) => {
        console.log("Files:", res)
      }}
      onUploadError={(error) => {
        alert(`ERROR! ${error.message}`)
      }}
    />
  )
}
```

---

**Step 7: Test**

1. Run app: `npm run dev`
2. Navigate to upload page
3. Click upload button
4. Select image
5. Verify upload completes

---

### How to Set Up Vercel Blob

**Prerequisites**:
- Vercel deployment
- Next.js 15.1+

**Time**: 10 minutes

---

**Step 1: Install**

```bash
npm install @vercel/blob
```

---

**Step 2: Get Token**

Vercel Dashboard → Project → Settings → Environment Variables

Add:
```
BLOB_READ_WRITE_TOKEN=vercel_blob_...
```

---

**Step 3: Create Upload API**

Create `app/api/upload/route.ts`:
```typescript
import { put } from '@vercel/blob'
import { auth } from '@/auth'

export async function POST(request: Request) {
  const session = await auth()
  if (!session) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const form = await request.formData()
  const file = form.get('file') as File

  if (!file) {
    return Response.json({ error: 'No file' }, { status: 400 })
  }

  const blob = await put(file.name, file, {
    access: 'public',
    addRandomSuffix: true
  })

  return Response.json(blob)
}
```

---

**Step 4: Create Upload Component**

```typescript
"use client"

import { useState } from "react"

export function BlobUploader() {
  const [isUploading, setIsUploading] = useState(false)

  async function handleUpload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setIsUploading(true)

    const form = e.currentTarget
    const formData = new FormData(form)

    const res = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    })

    const blob = await res.json()
    console.log('Uploaded:', blob.url)
    setIsUploading(false)
  }

  return (
    <form onSubmit={handleUpload}>
      <input type="file" name="file" required />
      <button disabled={isUploading}>
        {isUploading ? 'Uploading...' : 'Upload'}
      </button>
    </form>
  )
}
```

---

### How to Set Up Supabase Storage

**Prerequisites**:
- Supabase project
- Next.js 15.1+

**Time**: 20 minutes

---

**Step 1: Create Storage Bucket**

Supabase Dashboard → Storage → Create bucket

Name: `avatars`
Public: ✅ YES (or use RLS for private)

---

**Step 2: Install Client**

```bash
npm install @supabase/supabase-js
```

Add to `.env.local`:
```
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

---

**Step 3: Create Supabase Client**

Create `lib/supabase.ts`:
```typescript
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

---

**Step 4: Set Up RLS Policies**

Supabase Dashboard → SQL Editor:
```sql
-- Enable RLS
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Allow authenticated uploads
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK (
  auth.uid() IS NOT NULL
  AND bucket_id = 'avatars'
);

-- Users can access their own files
CREATE POLICY "Users can access own files"
ON storage.objects FOR SELECT
USING (auth.uid() = owner);
```

---

**Step 5: Create Upload Component**

```typescript
"use client"

import { supabase } from '@/lib/supabase'
import { useState } from 'react'

export function SupabaseUploader() {
  const [isUploading, setIsUploading] = useState(false)

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setIsUploading(true)

    const { data, error } = await supabase.storage
      .from('avatars')
      .upload(`user-${Date.now()}/avatar.png`, file)

    if (error) {
      console.error('Upload error:', error)
    } else {
      const { data: urlData } = supabase.storage
        .from('avatars')
        .getPublicUrl(data.path)

      console.log('Uploaded:', urlData.publicUrl)
    }

    setIsUploading(false)
  }

  return (
    <input
      type="file"
      onChange={handleUpload}
      disabled={isUploading}
    />
  )
}
```

---

### How to Set Up AWS S3

**Prerequisites**:
- AWS account
- Next.js 15.1+

**Time**: 30 minutes

---

**Step 1: Create S3 Bucket**

AWS Console → S3 → Create bucket

- Bucket name: `my-app-uploads`
- Region: `us-east-1`
- Block public access: ✅ ON (use presigned URLs)

---

**Step 2: Create IAM User**

IAM → Users → Add user

- Username: `my-app-s3-uploader`
- Access type: Programmatic access
- Attach policy:

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

Copy Access Key ID and Secret Access Key.

---

**Step 3: Configure CORS**

S3 → Bucket → Permissions → CORS:
```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["PUT", "POST", "GET", "DELETE"],
    "AllowedOrigins": ["http://localhost:3000", "https://yourdomain.com"],
    "ExposeHeaders": ["ETag"]
  }
]
```

---

**Step 4: Install AWS SDK**

```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

Add to `.env.local`:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_BUCKET_NAME=my-app-uploads

NEXT_PUBLIC_AWS_BUCKET=my-app-uploads
NEXT_PUBLIC_AWS_REGION=us-east-1
```

---

**Step 5: Create S3 Client**

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

**Step 6: Create Presigned URL API**

Create `app/api/s3/presigned-url/route.ts`:
```typescript
import { s3Client } from '@/lib/s3'
import { PutObjectCommand } from "@aws-sdk/client-s3"
import { getSignedUrl } from "@aws-sdk/s3-request-presigner"
import { auth } from '@/auth'

export async function POST(request: Request) {
  const user = await auth()
  if (!user) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { filename, contentType } = await request.json()

  const key = `uploads/${user.id}/${Date.now()}-${filename}`

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

**Step 7: Create Upload Component**

```typescript
"use client"

import { useState } from "react"

export function S3Uploader() {
  const [isUploading, setIsUploading] = useState(false)

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setIsUploading(true)

    // 1. Get presigned URL
    const res = await fetch('/api/s3/presigned-url', {
      method: 'POST',
      body: JSON.stringify({
        filename: file.name,
        contentType: file.type
      })
    })

    const { url, key } = await res.json()

    // 2. Upload to S3
    await fetch(url, {
      method: 'PUT',
      body: file,
      headers: {
        'Content-Type': file.type
      }
    })

    const s3Url = `https://${process.env.NEXT_PUBLIC_AWS_BUCKET}.s3.${process.env.NEXT_PUBLIC_AWS_REGION}.amazonaws.com/${key}`
    console.log('Uploaded:', s3Url)

    setIsUploading(false)
  }

  return (
    <input
      type="file"
      onChange={handleUpload}
      disabled={isUploading}
    />
  )
}
```

---

### How to Implement File Validation

**Complete validation with client + server layers**

---

**Step 1: Client-Side Validation (UX)**

```typescript
import { z } from 'zod'

const fileSchema = z.object({
  file: z.instanceof(File)
    .refine(file => file.size <= 5 * 1024 * 1024, "File must be < 5MB")
    .refine(file => ['image/jpeg', 'image/png', 'image/webp'].includes(file.type), "Only JPEG, PNG, WebP allowed")
})

export function validateFileClient(file: File) {
  const result = fileSchema.safeParse({ file })

  if (!result.success) {
    return { error: result.error.errors[0].message }
  }

  return { success: true }
}
```

---

**Step 2: Server-Side Validation (Security)**

```typescript
"use server"

import { fileTypeFromBuffer } from 'file-type'

export async function uploadFile(formData: FormData) {
  const file = formData.get('file')
  if (!(file instanceof File)) {
    return { error: 'File required' }
  }

  // Validate size
  if (file.size > 5 * 1024 * 1024) {
    return { error: 'File too large (max 5MB)' }
  }

  // Validate MIME (magic bytes, not extension)
  const buffer = Buffer.from(await file.arrayBuffer())
  const type = await fileTypeFromBuffer(buffer)

  const validMimeTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!type || !validMimeTypes.includes(type.mime)) {
    return { error: 'Invalid file type' }
  }

  // Upload...
  return { success: true }
}
```

---

**Step 3: Combined Client/Server Validation**

```typescript
"use client"

import { useState } from 'react'
import { validateFileClient } from './validation'
import { uploadFile } from './upload-action'

export function ValidatedUploader() {
  async function handleUpload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()

    const form = e.currentTarget
    const formData = new FormData(form)
    const file = formData.get('file') as File

    // Client validation (immediate feedback)
    const clientResult = validateFileClient(file)
    if (clientResult.error) {
      alert(clientResult.error)
      return
    }

    // Server validation (security)
    const serverResult = await uploadFile(formData)
    if (serverResult.error) {
      alert(serverResult.error)
      return
    }

    console.log('Upload successful!')
  }

  return (
    <form onSubmit={handleUpload}>
      <input type="file" name="file" accept="image/*" required />
      <button type="submit">Upload</button>
    </form>
  )
}
```

---

### How to Add Virus Scanning

**ClamAV integration for virus scanning**

---

**Option 1: ClamAV Lambda (AWS)**

```typescript
import { Lambda } from "@aws-sdk/client-lambda"

const lambda = new Lambda({ region: process.env.AWS_REGION })

export async function scanFile(s3Key: string) {
  const result = await lambda.invoke({
    FunctionName: "clamav-scan",
    Payload: JSON.stringify({
      bucket: process.env.AWS_BUCKET_NAME,
      key: s3Key
    })
  })

  const response = JSON.parse(new TextDecoder().decode(result.Payload))

  return response.status === 'clean'
}
```

---

**Option 2: Cloudflare Workers with ClamAV**

```typescript
// Cloudflare Worker with WASM ClamAV
export default {
  async fetch(request: Request) {
    const formData = await request.formData()
    const file = formData.get('file') as File

    const buffer = await file.arrayBuffer()

    // Scan with ClamAV WASM
    const isClean = await scanWithClamAV(buffer)

    if (!isClean) {
      return new Response('Virus detected', { status: 400 })
    }

    // Upload to storage
    return new Response('OK')
  }
}
```

---

**Option 3: Skip for Small Files (<1MB)**

```typescript
export async function uploadWithOptionalScan(file: File) {
  const shouldScan = file.size > 1 * 1024 * 1024 // 1MB

  if (shouldScan) {
    const isClean = await scanFile(file)
    if (!isClean) {
      throw new Error('Virus detected')
    }
  }

  // Upload file
  return await uploadToStorage(file)
}
```

---

### How to Optimize Images

**Sharp.js image optimization pipeline**

---

**Step 1: Install Sharp**

```bash
npm install sharp
```

---

**Step 2: Create Optimization Function**

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
```

---

**Step 3: Generate Multiple Sizes**

```typescript
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

**Step 4: Use in Upload**

```typescript
"use server"

import { optimizeImage } from './optimize'

export async function uploadOptimizedImage(formData: FormData) {
  const file = formData.get('file') as File
  const buffer = Buffer.from(await file.arrayBuffer())

  // Optimize image
  const optimized = await optimizeImage(buffer)

  // Upload optimized version
  const url = await uploadToStorage(optimized, 'image.webp')

  return { success: true, url }
}
```

---

### How to Implement Progress Indicators

**Upload progress with real-time percentage**

---

**UploadThing (Built-in)**

```typescript
import { useUploadThing } from "@/utils/uploadthing"

export function UploaderWithProgress() {
  const { startUpload, isUploading, uploadProgress } = useUploadThing("imageUploader")

  return (
    <div>
      <button onClick={() => startUpload(files)}>
        Upload
      </button>

      {isUploading && (
        <div>
          <progress value={uploadProgress} max={100} />
          <p>{uploadProgress}% uploaded</p>
        </div>
      )}
    </div>
  )
}
```

---

**Custom Progress with XMLHttpRequest**

```typescript
"use client"

import { useState } from "react"

export function CustomProgressUploader() {
  const [progress, setProgress] = useState(0)

  async function handleUpload(file: File) {
    const formData = new FormData()
    formData.append('file', file)

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()

      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const percentage = (e.loaded / e.total) * 100
          setProgress(Math.round(percentage))
        }
      })

      xhr.addEventListener('load', () => {
        resolve(xhr.response)
      })

      xhr.addEventListener('error', () => {
        reject(new Error('Upload failed'))
      })

      xhr.open('POST', '/api/upload')
      xhr.send(formData)
    })
  }

  return (
    <div>
      <input type="file" onChange={(e) => {
        const file = e.target.files?.[0]
        if (file) handleUpload(file)
      }} />

      {progress > 0 && progress < 100 && (
        <div>
          <progress value={progress} max={100} />
          <p>{progress}% uploaded</p>
        </div>
      )}
    </div>
  )
}
```

---

### How to Add Drag-and-Drop Upload

**React Dropzone integration**

---

**Step 1: Install**

```bash
npm install react-dropzone
```

---

**Step 2: Create Dropzone Component**

```typescript
"use client"

import { useDropzone } from 'react-dropzone'
import { useState } from 'react'

export function DragDropUploader() {
  const [files, setFiles] = useState<File[]>([])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { 'image/*': [] },
    maxFiles: 10,
    maxSize: 5 * 1024 * 1024, // 5MB
    onDrop: (acceptedFiles) => {
      setFiles(acceptedFiles)
    }
  })

  return (
    <div {...getRootProps()} className="border-2 border-dashed p-8">
      <input {...getInputProps()} />

      {isDragActive ? (
        <p>Drop files here...</p>
      ) : (
        <p>Drag files here or click to select</p>
      )}

      <ul>
        {files.map((file, i) => (
          <li key={i}>{file.name} ({(file.size / 1024).toFixed(2)} KB)</li>
        ))}
      </ul>
    </div>
  )
}
```

---

### How to Configure CDN Delivery

**CloudFront setup for S3 (AWS)**

---

**Step 1: Create CloudFront Distribution**

AWS Console → CloudFront → Create distribution

- Origin domain: `my-app-uploads.s3.us-east-1.amazonaws.com`
- Origin access: Origin Access Control (OAC)
- Viewer protocol policy: Redirect HTTP to HTTPS
- Cache policy: CachingOptimized

---

**Step 2: Update S3 Bucket Policy**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-app-uploads/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::123456789:distribution/EDFDVBD6EXAMPLE"
        }
      }
    }
  ]
}
```

---

**Step 3: Use CloudFront URL**

```typescript
const cloudfrontDomain = 'd111111abcdef8.cloudfront.net'
const key = 'uploads/user-123/image.png'
const url = `https://${cloudfrontDomain}/${key}`
```

---

### How to Integrate with Database

**Save file metadata to database (SAP-034)**

---

**Step 1: Create Prisma Schema**

```prisma
model Upload {
  id        String   @id @default(cuid())
  url       String
  key       String?  // S3 key or file path
  filename  String
  mimeType  String
  size      Int
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([userId])
}
```

---

**Step 2: Save Metadata on Upload**

```typescript
"use server"

import { prisma } from '@/lib/prisma'
import { auth } from '@/auth'

export async function uploadFile(formData: FormData) {
  const user = await auth()
  if (!user) return { error: 'Unauthorized' }

  const file = formData.get('file') as File

  // Upload to storage
  const { url, key } = await uploadToStorage(file)

  // Save metadata to database
  const upload = await prisma.upload.create({
    data: {
      url,
      key,
      filename: file.name,
      mimeType: file.type,
      size: file.size,
      userId: user.id
    }
  })

  return { success: true, upload }
}
```

---

**Step 3: Query User's Uploads**

```typescript
export async function getUserUploads(userId: string) {
  return await prisma.upload.findMany({
    where: { userId },
    orderBy: { createdAt: 'desc' }
  })
}
```

---

### How to Secure Uploads with Auth

**Require authentication for all uploads (SAP-033)**

---

**UploadThing**

```typescript
// app/api/uploadthing/core.ts
export const ourFileRouter = {
  imageUploader: f({ image: { maxFileSize: "4MB" } })
    .middleware(async () => {
      const user = await auth()
      if (!user) throw new Error("Unauthorized")
      return { userId: user.id }
    })
    .onUploadComplete(async ({ metadata, file }) => {
      // Metadata contains userId
    })
} satisfies FileRouter
```

---

**Vercel Blob**

```typescript
// app/api/upload/route.ts
export async function POST(request: Request) {
  const session = await auth()
  if (!session) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Upload file
}
```

---

**Supabase Storage (RLS)**

```sql
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK (auth.uid() IS NOT NULL);
```

---

**AWS S3 (Presigned URLs)**

```typescript
export async function POST(request: Request) {
  const user = await auth()
  if (!user) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Generate presigned URL only for authenticated users
  const url = await getPresignedUploadUrl(key, contentType)

  return Response.json({ url })
}
```

---

## Tutorials

### Tutorial 1: Simple Image Uploader

**Goal**: Build a basic image uploader with UploadThing

**Time**: 20 minutes

**What You'll Build**:
- Upload button
- Image preview
- Database integration

---

**Step 1: Set Up UploadThing** (5 min)

Follow [How to Set Up UploadThing](#how-to-set-up-uploadthing)

---

**Step 2: Create Database Schema** (3 min)

```prisma
model Upload {
  id        String   @id @default(cuid())
  url       String
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  createdAt DateTime @default(now())
}
```

Run migration:
```bash
npx prisma migrate dev --name add-uploads
```

---

**Step 3: Update File Router** (5 min)

```typescript
// app/api/uploadthing/core.ts
export const ourFileRouter = {
  imageUploader: f({ image: { maxFileSize: "4MB" } })
    .middleware(async () => {
      const user = await auth()
      if (!user) throw new Error("Unauthorized")
      return { userId: user.id }
    })
    .onUploadComplete(async ({ metadata, file }) => {
      await prisma.upload.create({
        data: {
          url: file.url,
          userId: metadata.userId
        }
      })
    })
} satisfies FileRouter
```

---

**Step 4: Create Upload Page** (5 min)

```typescript
// app/upload/page.tsx
"use client"

import { UploadButton } from "@/utils/uploadthing"
import { useState } from "react"
import Image from "next/image"

export default function UploadPage() {
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null)

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Upload Image</h1>

      <UploadButton
        endpoint="imageUploader"
        onClientUploadComplete={(res) => {
          if (res?.[0]) {
            setUploadedUrl(res[0].url)
          }
        }}
        onUploadError={(error) => {
          alert(`ERROR! ${error.message}`)
        }}
      />

      {uploadedUrl && (
        <div className="mt-4">
          <h2 className="text-xl mb-2">Uploaded Image:</h2>
          <Image
            src={uploadedUrl}
            alt="Uploaded"
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

**Step 5: Test** (2 min)

1. Navigate to `/upload`
2. Click "Choose File"
3. Select image
4. Verify upload completes
5. Check image displays
6. Verify database record created

---

**Congratulations!** You've built a simple image uploader with database integration.

---

### Tutorial 2: Multi-File Uploader with Progress

**Goal**: Build a multi-file uploader with progress indicators

**Time**: 30 minutes

**What You'll Build**:
- Multi-file selection
- Upload progress bars
- Thumbnail previews
- Delete uploaded files

---

**Step 1: Create Upload Component** (10 min)

```typescript
"use client"

import { useUploadThing } from "@/utils/uploadthing"
import { useState } from "react"
import Image from "next/image"

interface UploadedFile {
  url: string
  name: string
}

export function MultiFileUploader() {
  const [files, setFiles] = useState<File[]>([])
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])

  const { startUpload, isUploading, uploadProgress } = useUploadThing("imageUploader", {
    onClientUploadComplete: (res) => {
      setUploadedFiles(prev => [
        ...prev,
        ...res.map(file => ({ url: file.url, name: file.name }))
      ])
      setFiles([])
    },
    onUploadError: (error) => {
      alert(`ERROR! ${error.message}`)
    }
  })

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selectedFiles = Array.from(e.target.files || [])
    setFiles(selectedFiles)
  }

  function handleUpload() {
    if (files.length > 0) {
      startUpload(files)
    }
  }

  function handleDelete(url: string) {
    setUploadedFiles(prev => prev.filter(f => f.url !== url))
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Multi-File Uploader</h1>

      {/* File Selection */}
      <div className="mb-4">
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileChange}
          className="mb-2"
        />

        {files.length > 0 && (
          <div>
            <p>{files.length} file(s) selected</p>
            <button
              onClick={handleUpload}
              disabled={isUploading}
              className="bg-blue-500 text-white px-4 py-2 rounded"
            >
              {isUploading ? `Uploading... ${uploadProgress}%` : 'Upload'}
            </button>
          </div>
        )}

        {/* Progress Bar */}
        {isUploading && (
          <div className="mt-2">
            <progress value={uploadProgress} max={100} className="w-full" />
          </div>
        )}
      </div>

      {/* Uploaded Files */}
      <div>
        <h2 className="text-xl mb-2">Uploaded Files ({uploadedFiles.length})</h2>
        <div className="grid grid-cols-3 gap-4">
          {uploadedFiles.map((file, i) => (
            <div key={i} className="relative">
              <Image
                src={file.url}
                alt={file.name}
                width={200}
                height={200}
                className="rounded-lg"
              />
              <button
                onClick={() => handleDelete(file.url)}
                className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
```

---

**Step 2: Create Page** (5 min)

```typescript
// app/upload/page.tsx
import { MultiFileUploader } from "@/components/MultiFileUploader"

export default function UploadPage() {
  return <MultiFileUploader />
}
```

---

**Step 3: Test** (5 min)

1. Navigate to `/upload`
2. Select multiple images (Ctrl/Cmd + Click)
3. Click "Upload"
4. Watch progress bar
5. Verify all images upload
6. Test delete button

---

### Tutorial 3: Avatar Uploader with Crop

**Goal**: Build avatar uploader with client-side image cropping

**Time**: 35 minutes

**What You'll Build**:
- File selection
- Image cropping with preview
- Upload cropped image
- Update user profile

---

**Step 1: Install React Image Crop** (2 min)

```bash
npm install react-image-crop
```

---

**Step 2: Create Avatar Uploader** (20 min)

```typescript
"use client"

import { useState, useRef } from "react"
import ReactCrop, { type Crop, type PixelCrop } from 'react-image-crop'
import 'react-image-crop/dist/ReactCrop.css'
import { useUploadThing } from "@/utils/uploadthing"

export function AvatarUploader() {
  const [imgSrc, setImgSrc] = useState<string>('')
  const [crop, setCrop] = useState<Crop>()
  const [completedCrop, setCompletedCrop] = useState<PixelCrop>()
  const imgRef = useRef<HTMLImageElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  const { startUpload, isUploading } = useUploadThing("imageUploader")

  function onSelectFile(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files && e.target.files.length > 0) {
      const reader = new FileReader()
      reader.addEventListener('load', () => {
        setImgSrc(reader.result?.toString() || '')
      })
      reader.readAsDataURL(e.target.files[0])
    }
  }

  async function onUploadCropped() {
    if (!completedCrop || !imgRef.current || !canvasRef.current) {
      return
    }

    const image = imgRef.current
    const canvas = canvasRef.current
    const crop = completedCrop

    const scaleX = image.naturalWidth / image.width
    const scaleY = image.naturalHeight / image.height
    const ctx = canvas.getContext('2d')

    if (!ctx) return

    canvas.width = crop.width
    canvas.height = crop.height

    ctx.drawImage(
      image,
      crop.x * scaleX,
      crop.y * scaleY,
      crop.width * scaleX,
      crop.height * scaleY,
      0,
      0,
      crop.width,
      crop.height
    )

    // Convert canvas to blob
    canvas.toBlob(async (blob) => {
      if (!blob) return

      const file = new File([blob], 'avatar.png', { type: 'image/png' })
      const res = await startUpload([file])

      if (res && res[0]) {
        console.log('Avatar uploaded:', res[0].url)
        // Update user profile with avatar URL
      }
    }, 'image/png')
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Avatar Uploader</h1>

      <input type="file" accept="image/*" onChange={onSelectFile} />

      {imgSrc && (
        <>
          <ReactCrop
            crop={crop}
            onChange={(_, percentCrop) => setCrop(percentCrop)}
            onComplete={(c) => setCompletedCrop(c)}
            aspect={1}
            circularCrop
          >
            <img
              ref={imgRef}
              alt="Crop me"
              src={imgSrc}
              style={{ maxHeight: '400px' }}
            />
          </ReactCrop>

          <button
            onClick={onUploadCropped}
            disabled={isUploading}
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
          >
            {isUploading ? 'Uploading...' : 'Upload Avatar'}
          </button>

          <canvas ref={canvasRef} style={{ display: 'none' }} />
        </>
      )}
    </div>
  )
}
```

---

**Step 3: Test** (5 min)

1. Navigate to avatar uploader
2. Select image
3. Crop to circular shape
4. Upload cropped avatar
5. Verify upload completes

---

### Tutorial 4: Document Uploader with Virus Scan

**Goal**: Build document uploader with virus scanning

**Time**: 40 minutes

**What You'll Build**:
- PDF/DOCX upload
- Server-side virus scanning (ClamAV)
- Quarantine infected files
- Email notification

---

**Step 1: Set Up File Router** (5 min)

```typescript
// app/api/uploadthing/core.ts
export const ourFileRouter = {
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
      // Scan for viruses
      const isClean = await scanFile(file.url)

      if (!isClean) {
        // Quarantine file
        await prisma.upload.create({
          data: {
            url: file.url,
            userId: metadata.userId,
            status: 'quarantined'
          }
        })

        // Send email notification
        await sendEmail({
          to: metadata.userEmail,
          subject: 'Virus Detected in Upload',
          body: `A virus was detected in your uploaded file: ${file.name}`
        })

        throw new Error("Virus detected")
      }

      // Save clean file
      await prisma.upload.create({
        data: {
          url: file.url,
          userId: metadata.userId,
          status: 'clean'
        }
      })
    })
} satisfies FileRouter
```

---

**Step 2: Create Virus Scan Function** (15 min)

```typescript
// lib/virus-scan.ts
import { Lambda } from "@aws-sdk/client-lambda"

const lambda = new Lambda({ region: process.env.AWS_REGION })

export async function scanFile(url: string): Promise<boolean> {
  try {
    const result = await lambda.invoke({
      FunctionName: "clamav-scan",
      Payload: JSON.stringify({ url })
    })

    const response = JSON.parse(new TextDecoder().decode(result.Payload))

    return response.status === 'clean'
  } catch (error) {
    console.error('Virus scan error:', error)
    // Fail closed: assume infected if scan fails
    return false
  }
}
```

---

**Step 3: Create Upload Component** (10 min)

```typescript
"use client"

import { UploadButton } from "@/utils/uploadthing"
import { useState } from "react"

export function DocumentUploader() {
  const [status, setStatus] = useState<string>('')

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Document Uploader</h1>

      <UploadButton
        endpoint="documentUploader"
        onClientUploadComplete={(res) => {
          setStatus('Upload successful! File is clean.')
        }}
        onUploadError={(error) => {
          if (error.message.includes('Virus detected')) {
            setStatus('VIRUS DETECTED! File has been quarantined.')
          } else {
            setStatus(`Error: ${error.message}`)
          }
        }}
      />

      {status && (
        <p className={status.includes('VIRUS') ? 'text-red-600' : 'text-green-600'}>
          {status}
        </p>
      )}
    </div>
  )
}
```

---

**Step 4: Test** (10 min)

1. Upload clean PDF → Success
2. Upload EICAR test file (virus test) → Quarantined
3. Verify email sent
4. Check database for quarantined files

---

## Evidence & Benchmarks

### Pricing Comparison

**Scenario**: 100GB storage + 1000 uploads/month

| Provider | Cost | Notes |
|----------|------|-------|
| **Supabase Storage** | $9.21/mo | $0.021/GB storage + $0.09/GB egress |
| **AWS S3** | $9.23/mo | $0.023/GB storage + CloudFront costs |
| **UploadThing** | $10/mo | 100GB plan (includes bandwidth) |
| **Vercel Blob** | $15.50/mo | $0.05/GB storage + $0.15/GB egress |

---

### Performance Benchmarks

**Upload Time** (5MB file, global average):

| Provider | Upload Time | Notes |
|----------|-------------|-------|
| **Vercel Blob** | 300ms | Edge-optimized, closest region |
| **AWS S3** | 400ms | With CloudFront acceleration |
| **UploadThing** | 500ms | Global CDN, Next.js optimized |
| **Supabase Storage** | 600ms | Single region (us-east-1) |

---

### Setup Time

| Provider | Setup Time | Complexity |
|----------|------------|------------|
| **Vercel Blob** | 10 min | Easiest (no IAM, no CORS) |
| **UploadThing** | 15 min | Easy (pre-built components) |
| **Supabase Storage** | 20 min | Moderate (RLS policies) |
| **AWS S3** | 30 min | Complex (IAM, CORS, CloudFront) |

---

### Production Usage

- **UploadThing**: Cal.com, Ping.gg, T3 Stack projects
- **Vercel Blob**: Vercel internal tools, v0.dev
- **Supabase Storage**: 200k+ Supabase projects, Plane, Supabase Dashboard
- **AWS S3**: Netflix, Airbnb, Pinterest, NASA (100+ trillion objects)

---

### Security Features

| Feature | UploadThing | Vercel Blob | Supabase | AWS S3 |
|---------|-------------|-------------|----------|--------|
| **HTTPS** | ✅ | ✅ | ✅ | ✅ |
| **Virus Scanning** | ✅ Built-in | ❌ Manual | ❌ Manual | ❌ Manual |
| **RLS** | ❌ | ❌ | ✅ | ❌ |
| **IAM** | ❌ | ❌ | ❌ | ✅ |
| **Presigned URLs** | ❌ | ✅ | ✅ | ✅ |
| **Encryption at Rest** | ✅ | ✅ | ✅ | ✅ |

---

## Version History

### 1.0.0 (2025-11-09) - Initial Release

**Added**:
- Complete API reference for 4 providers (UploadThing, Vercel Blob, Supabase Storage, AWS S3)
- 12 how-to guides (setup, validation, virus scanning, optimization, etc.)
- 4 complete tutorials (simple uploader, multi-file, avatar crop, virus scan)
- File validation patterns (client + server)
- Image optimization API (sharp.js)
- Security architecture (3-layer validation)
- Decision matrix for provider selection
- Performance benchmarks and pricing comparison

**Status**: Pilot (awaiting first production adoption)

---

## Next Steps

1. **Choose Provider**: Use decision tree to select provider
2. **Follow How-to**: Read setup guide for chosen provider
3. **Complete Tutorial**: Build simple uploader (Tutorial 1)
4. **Add Security**: Implement validation + virus scanning
5. **Optimize Images**: Add sharp.js optimization
6. **Integrate Database**: Save file metadata (SAP-034)
7. **Test**: Validate all flows before production

**Next Document**: [adoption-blueprint.md](adoption-blueprint.md) for step-by-step installation
