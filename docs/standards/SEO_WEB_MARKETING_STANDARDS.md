# SEO & Web Marketing Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** SEO

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Focus:** Technical SEO, performance optimization, and marketing automation

## Table of Contents

1. [Technical SEO Foundations](#1-technical-seo-foundations)
2. [On-Page Optimization](#2-on-page-optimization)
3. [Site Architecture and Navigation](#3-site-architecture-and-navigation)
4. [Performance and Core Web Vitals](#4-performance-and-core-web-vitals)
5. [Schema and Structured Data](#5-schema-and-structured-data)
6. [Content Marketing Technical Standards](#6-content-marketing-technical-standards)
7. [Analytics and Tracking](#7-analytics-and-tracking)
8. [Marketing Automation](#8-marketing-automation)
9. [Email Marketing Standards](#9-email-marketing-standards)
10. [Implementation Guidelines](#10-implementation-guidelines)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Technical SEO Foundations

### 1.1 Crawlability and Indexability **[REQUIRED]**

```yaml
crawlability_standards:
  robots_txt:
    location: "/robots.txt"
    requirements:
      - Accessible at root domain
      - Valid syntax
      - Sitemap reference
      - Crawl-delay if needed

    example: |
      User-agent: *
      Allow: /
      Disallow: /api/
      Disallow: /admin/
      Sitemap: https://example.com/sitemap.xml

  xml_sitemap:
    requirements:
      - Maximum 50,000 URLs per file
      - Under 50MB uncompressed
      - UTF-8 encoding
      - Update frequency accurate

    structure:
      main: "/sitemap.xml"
      index: "/sitemap-index.xml"
      types:
        - pages: "/sitemap-pages.xml"
        - posts: "/sitemap-posts.xml"
        - images: "/sitemap-images.xml"
        - videos: "/sitemap-videos.xml"

  crawl_optimization:
    - Remove crawl traps
    - Fix redirect chains
    - Eliminate duplicate content
    - Implement pagination correctly
```

### 1.2 URL Structure **[REQUIRED]**

```yaml
url_standards:
  structure:
    format: "https://domain.com/category/subcategory/page-name"
    rules:
      - Lowercase only
      - Hyphens for word separation
      - No special characters
      - Maximum 60 characters
      - Descriptive keywords

  implementation:
    canonical_urls:
      - Self-referencing canonicals
      - Cross-domain canonicals
      - Parameter handling
      - Protocol consistency

    redirects:
      types:
        301: "Permanent moves"
        302: "Temporary redirects"
        308: "Permanent (preserve method)"

      rules:
        - Maximum 2 redirect hops
        - Update internal links
        - Monitor redirect chains
        - Log all redirects

  internationalization:
    hreflang:
      implementation: "Link tags in head"
      format: '<link rel="alternate" hreflang="en-us" href="...">'
      requirements:
        - Bidirectional references
        - Include x-default
        - Absolute URLs
        - Valid language codes
```

### 1.3 HTTPS and Security **[REQUIRED]**

```yaml
security_seo:
  ssl_requirements:
    certificate:
      - Valid SSL certificate
      - Minimum TLS 1.2
      - HSTS enabled
      - No mixed content

    implementation:
      server_config: |
        # HSTS with preload
        Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

        # Security headers
        X-Content-Type-Options: nosniff
        X-Frame-Options: SAMEORIGIN
        Referrer-Policy: strict-origin-when-cross-origin

  csp_for_seo:
    balance:
      - Allow necessary third-party scripts
      - Permit analytics tools
      - Enable social widgets
      - Maintain security
```

---

## 2. On-Page Optimization

### 2.1 Meta Tags Optimization **[REQUIRED]**

```yaml
meta_tags:
  title_tag:
    requirements:
      length: "50-60 characters"
      structure: "Primary Keyword - Secondary Keyword | Brand"
      uniqueness: "Unique per page"

    implementation:
      dynamic_generation: |
        <title>{pageTitle} | {categoryName} | {siteName}</title>

  meta_description:
    requirements:
      length: "150-160 characters"
      cta: "Include call-to-action"
      keywords: "Natural inclusion"
      uniqueness: "Unique per page"

    template: |
      <meta name="description" content="{summary}. {benefit}. {cta}">

  open_graph:
    required_tags:
      - og:title
      - og:description
      - og:image
      - og:url
      - og:type

    image_specs:
      dimensions: "1200x630px"
      format: "JPG or PNG"
      size: "< 5MB"

  twitter_cards:
    types:
      summary: "Default card"
      summary_large_image: "Featured content"
      player: "Video content"

    required:
      - twitter:card
      - twitter:title
      - twitter:description
      - twitter:image
```

### 2.2 Header Tag Hierarchy **[REQUIRED]**

```yaml
header_structure:
  hierarchy:
    h1:
      count: "One per page"
      placement: "Above fold"
      keywords: "Primary keyword included"

    h2_h6:
      structure: "Logical hierarchy"
      keywords: "LSI keywords"
      nesting: "Proper parent-child"

  implementation:
    semantic_html:
      - Use heading tags for structure
      - Don't skip levels
      - Include keywords naturally
      - Support outline algorithm

    accessibility:
      - Screen reader friendly
      - Logical flow
      - Descriptive headings
```

### 2.3 Content Optimization **[REQUIRED]**

```yaml
content_standards:
  keyword_optimization:
    density: "1-2% for primary"
    placement:
      - Title tag
      - First paragraph
      - H1 tag
      - Alt text
      - Meta description

    lsi_keywords:
      - Related terms
      - Synonyms
      - Entity mentions
      - Question variations

  content_structure:
    requirements:
      - Minimum 300 words
      - Original content
      - E-A-T signals
      - Regular updates

    formatting:
      - Short paragraphs (2-3 sentences)
      - Bullet points
      - Numbered lists
      - Bold key phrases

  internal_linking:
    strategy:
      - 3-5 internal links per page
      - Descriptive anchor text
      - Relevant context
      - Deep linking

    implementation:
      - Automated related posts
      - Contextual links
      - Navigation links
      - Footer links
```

---

## 3. Site Architecture and Navigation

### 3.1 Information Architecture **[REQUIRED]**

```yaml
site_architecture:
  hierarchy:
    depth: "Maximum 3 clicks from homepage"
    structure:
      - Homepage
      - Category pages
      - Subcategory pages
      - Product/content pages

  navigation:
    main_menu:
      - 7±2 items maximum
      - Descriptive labels
      - Logical grouping
      - Mobile-friendly

    breadcrumbs:
      implementation: "Schema.org BreadcrumbList"
      format: "Home > Category > Subcategory > Page"
      requirements:
        - On all pages except home
        - Clickable links
        - Current page not linked

  url_architecture:
    patterns:
      blog: "/blog/category/post-title"
      product: "/products/category/product-name"
      service: "/services/service-name"
      location: "/locations/city/business-name"
```

### 3.2 Pagination Standards **[REQUIRED]**

```yaml
pagination:
  implementation:
    rel_tags:
      - rel="prev" for previous page
      - rel="next" for next page
      - Canonical to self on each page

    url_structure:
      format: "/category/page/2"
      avoid: "?page=2" when possible

  infinite_scroll:
    seo_friendly:
      - Provide paginated alternative
      - Implement history.pushState
      - Load content progressively
      - Include "View All" option

  optimization:
    - Index first page only
    - Consolidate thin pages
    - Implement view-all wisely
    - Monitor crawl budget
```

### 3.3 Mobile Optimization **[REQUIRED]**

```yaml
mobile_seo:
  responsive_design:
    requirements:
      - Mobile-first CSS
      - Flexible images
      - Viewport meta tag
      - Touch-friendly elements

    viewport_meta: |
      <meta name="viewport" content="width=device-width, initial-scale=1">

  mobile_usability:
    standards:
      - Tap targets: 48x48px minimum
      - Font size: 16px minimum
      - No horizontal scrolling
      - Fast loading (< 3s)

  amp_implementation:
    when_needed:
      - News articles
      - Blog posts
      - Product pages

    requirements:
      - Valid AMP HTML
      - Canonical reference
      - Structured data
      - Analytics tracking
```

---

## 4. Performance and Core Web Vitals

### 4.1 Core Web Vitals Optimization **[REQUIRED]**

```yaml
core_web_vitals:
  lcp_optimization:
    target: "< 2.5 seconds"
    techniques:
      - Optimize server response time
      - Preload critical resources
      - Optimize images and videos
      - Remove render-blocking resources

    implementation:
      preload_critical: |
        <link rel="preload" as="image" href="hero-image.webp">
        <link rel="preload" as="font" href="main-font.woff2" crossorigin>

  fid_optimization:
    target: "< 100 milliseconds"
    techniques:
      - Break up long tasks
      - Use web workers
      - Optimize JavaScript execution
      - Implement progressive enhancement

  cls_optimization:
    target: "< 0.1"
    techniques:
      - Size attributes on images/videos
      - Reserve space for ads
      - Avoid inserting content above
      - Font loading optimization

    implementation:
      image_dimensions: |
        <img src="..." width="800" height="600" alt="...">

      font_loading: |
        font-display: optional; /* or swap */
```

### 4.2 Page Speed Optimization **[REQUIRED]**

```yaml
performance_standards:
  resource_optimization:
    images:
      formats: ["WebP", "AVIF", "JPEG"]
      lazy_loading: "loading='lazy'"
      responsive: "srcset and sizes"
      compression: "85% quality"

    css:
      - Critical CSS inline
      - Non-critical deferred
      - Minification
      - Remove unused styles

    javascript:
      - Defer non-critical
      - Async where possible
      - Code splitting
      - Tree shaking

  caching_strategy:
    static_assets:
      images: "1 year"
      css_js: "1 year with versioning"
      fonts: "1 year"

    html:
      cache_control: "no-cache, must-revalidate"
      etag: "Enabled"

  cdn_configuration:
    requirements:
      - Global edge locations
      - HTTP/2 support
      - Brotli compression
      - Custom cache rules
```

### 4.3 Technical Performance **[REQUIRED]**

```yaml
technical_optimization:
  server_configuration:
    compression:
      - Enable Gzip/Brotli
      - Compress HTML, CSS, JS
      - Minimum 1KB threshold

    http2_http3:
      - Server push for critical resources
      - Multiplexing enabled
      - Header compression

  resource_hints:
    dns_prefetch: |
      <link rel="dns-prefetch" href="//cdn.example.com">

    preconnect: |
      <link rel="preconnect" href="https://fonts.googleapis.com">

    prefetch: |
      <link rel="prefetch" href="/next-page.html">

  critical_rendering_path:
    optimization:
      - Inline critical CSS
      - Defer JavaScript
      - Optimize web fonts
      - Prioritize visible content
```

---

## 5. Schema and Structured Data

### 5.1 Schema.org Implementation **[REQUIRED]**

```yaml
structured_data:
  formats:
    json_ld: "Recommended"
    microdata: "Legacy support"
    rdfa: "Avoid"

  common_schemas:
    organization:
      required:
        - name
        - url
        - logo
        - contactPoint
        - sameAs (social profiles)

    local_business:
      required:
        - name
        - address
        - telephone
        - openingHours
        - geo coordinates

    product:
      required:
        - name
        - image
        - description
        - offers (price, availability)
        - aggregateRating

    article:
      required:
        - headline
        - datePublished
        - author
        - image
        - publisher

  validation:
    tools:
      - Google Rich Results Test
      - Schema.org validator
      - Structured Data Testing Tool

    monitoring:
      - Search Console reports
      - Rich results status
      - Error tracking
```

### 5.2 Rich Snippets Optimization **[REQUIRED]**

```yaml
rich_snippets:
  types:
    faq:
      implementation: "FAQPage schema"
      requirements:
        - Question-answer pairs
        - Complete answers
        - No promotional content

    how_to:
      implementation: "HowTo schema"
      requirements:
        - Step-by-step instructions
        - Time estimates
        - Required tools/materials

    reviews:
      implementation: "Review/AggregateRating"
      requirements:
        - Genuine reviews
        - Rating scale
        - Review count

    events:
      implementation: "Event schema"
      requirements:
        - Event name
        - Start date/time
        - Location
        - Ticket information

  best_practices:
    - Test before deployment
    - Monitor performance
    - Update regularly
    - Follow guidelines
```

---

## 6. Content Marketing Technical Standards

### 6.1 Content Management **[REQUIRED]**

```yaml
content_management:
  content_types:
    blog_posts:
      url: "/blog/{category}/{slug}"
      metadata: [title, description, author, date]
      features: [comments, sharing, related]

    landing_pages:
      url: "/{campaign}/{offer}"
      elements: [hero, benefits, cta, form]
      tracking: [source, medium, campaign]

    resources:
      url: "/resources/{type}/{title}"
      types: [whitepapers, ebooks, guides]
      gating: "Progressive profiling"

  content_delivery:
    formats:
      - HTML pages
      - PDF downloads
      - Video embeds
      - Podcast feeds

    optimization:
      - CDN delivery
      - Responsive images
      - Lazy loading
      - Progressive enhancement
```

### 6.2 Content Syndication **[RECOMMENDED]**

```yaml
syndication:
  rss_feeds:
    implementation:
      main: "/feed.xml"
      category: "/category/{name}/feed.xml"

    requirements:
      - Valid XML
      - Full content or summary
      - Proper encoding
      - Update frequency

  social_sharing:
    meta_tags:
      - Open Graph
      - Twitter Cards
      - Pinterest Rich Pins

    implementation:
      - Share buttons
      - Click tracking
      - UTM parameters
      - Social proof

  cross_posting:
    canonical_handling:
      - Point to original
      - Avoid duplicate content
      - Track performance
```

---

## 7. Analytics and Tracking

### 7.1 Analytics Implementation **[REQUIRED]**

```yaml
analytics_setup:
  google_analytics_4:
    implementation:
      gtag: |
        <!-- Global site tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'GA_MEASUREMENT_ID');
        </script>

    enhanced_ecommerce:
      - Product impressions
      - Product clicks
      - Add to cart
      - Checkout steps
      - Purchase

    custom_dimensions:
      - Author
      - Category
      - User type
      - Content type

  goal_tracking:
    macro_conversions:
      - Form submissions
      - Phone calls
      - Purchases
      - Sign-ups

    micro_conversions:
      - PDF downloads
      - Video views
      - Tool usage
      - Social shares
```

### 7.2 Tag Management **[REQUIRED]**

```yaml
tag_management:
  google_tag_manager:
    container_setup:
      - Header container
      - Body container
      - DataLayer implementation
      - Version control

    common_tags:
      - Analytics tags
      - Conversion pixels
      - Remarketing tags
      - Heatmap tools

    triggers:
      - Page views
      - Clicks
      - Form submissions
      - Scroll depth
      - Time on page

  privacy_compliance:
    consent_management:
      - Cookie consent banner
      - Granular opt-in/out
      - Geographic detection
      - Preference center

    implementation:
      - Consent mode
      - Server-side tagging
      - Data retention
      - Anonymization
```

### 7.3 Conversion Tracking **[REQUIRED]**

```yaml
conversion_tracking:
  implementation:
    form_tracking:
      methods:
        - Thank you page
        - Event tracking
        - Callback functions
        - DataLayer pushes

    ecommerce_tracking:
      enhanced_ecommerce:
        - Product views
        - Cart actions
        - Checkout funnel
        - Transaction details

    phone_tracking:
      - Dynamic number insertion
      - Call tracking
      - Duration tracking
      - Source attribution

  attribution_models:
    types:
      - Last click
      - First click
      - Linear
      - Time decay
      - Data-driven

    implementation:
      - UTM parameters
      - Channel definitions
      - Campaign tagging
      - Cross-device tracking
```

---

## 8. Marketing Automation

### 8.1 Marketing Automation Setup **[RECOMMENDED]**

```yaml
marketing_automation:
  lead_capture:
    forms:
      progressive_profiling:
        - Basic info first
        - Additional fields over time
        - Smart field logic
        - Conditional questions

      optimization:
        - A/B testing
        - Field reduction
        - Inline validation
        - Mobile optimization

    landing_pages:
      elements:
        - Clear value proposition
        - Social proof
        - Trust signals
        - Minimal navigation

  lead_scoring:
    demographic:
      - Job title
      - Company size
      - Industry
      - Location

    behavioral:
      - Page views
      - Content downloads
      - Email engagement
      - Webinar attendance

    implementation:
      - Point assignment
      - Threshold setting
      - Score decay
      - Alert triggers
```

### 8.2 Workflow Automation **[RECOMMENDED]**

```yaml
automation_workflows:
  nurture_campaigns:
    welcome_series:
      - Welcome email (immediate)
      - Education (day 3)
      - Case study (day 7)
      - Offer (day 14)

    re_engagement:
      triggers:
        - 30 days inactive
        - Cart abandonment
        - Browse abandonment

  personalization:
    dynamic_content:
      - Industry-specific
      - Role-based
      - Stage-based
      - Behavior-based

    implementation:
      - Merge tags
      - Dynamic blocks
      - Smart content
      - AI recommendations
```

---

## 9. Email Marketing Standards

### 9.1 Email Technical Standards **[REQUIRED]**

```yaml
email_technical:
  deliverability:
    authentication:
      spf: "v=spf1 include:_spf.provider.com ~all"
      dkim: "2048-bit key minimum"
      dmarc: "v=DMARC1; p=quarantine; rua=mailto:..."

    reputation:
      - Warm up new IPs
      - Monitor blacklists
      - Manage bounce rates
      - Track complaints

  html_email:
    standards:
      - Tables for layout
      - Inline CSS
      - 600px max width
      - Alt text for images

    compatibility:
      - Test across clients
      - Fallback fonts
      - Dark mode support
      - Plain text version

  tracking:
    metrics:
      - Open rate
      - Click rate
      - Conversion rate
      - List growth rate

    implementation:
      - UTM parameters
      - Pixel tracking
      - Link wrapping
      - Conversion attribution
```

### 9.2 Email Optimization **[REQUIRED]**

```yaml
email_optimization:
  subject_lines:
    best_practices:
      - 30-50 characters
      - Personalization
      - A/B testing
      - Emoji usage (sparingly)

  preheader_text:
    requirements:
      - 40-100 characters
      - Complement subject
      - Call to action
      - Hidden if needed

  mobile_optimization:
    requirements:
      - Single column layout
      - Large tap targets (44x44px)
      - Readable fonts (14px+)
      - Compressed images

  accessibility:
    standards:
      - Semantic HTML
      - Alt text
      - Color contrast
      - Screen reader friendly
```

---

## 10. Implementation Guidelines

### 10.1 SEO Audit Checklist **[REQUIRED]**

```yaml
seo_audit:
  technical:
    - [ ] Crawlability check
    - [ ] XML sitemap valid
    - [ ] Robots.txt correct
    - [ ] HTTPS implementation
    - [ ] Page speed optimal
    - [ ] Mobile-friendly
    - [ ] Core Web Vitals pass

  on_page:
    - [ ] Title tags optimized
    - [ ] Meta descriptions unique
    - [ ] Header hierarchy correct
    - [ ] Internal linking strong
    - [ ] Image optimization
    - [ ] Schema markup valid

  content:
    - [ ] Keyword research done
    - [ ] Content quality high
    - [ ] E-A-T signals present
    - [ ] Fresh content strategy
    - [ ] User intent matched
```

### 10.2 Marketing Stack Integration **[RECOMMENDED]**

```yaml
marketing_stack:
  essential_tools:
    analytics:
      - Google Analytics 4
      - Google Search Console
      - Hotjar/Crazy Egg

    seo:
      - Screaming Frog
      - Ahrefs/SEMrush
      - PageSpeed Insights

    marketing:
      - HubSpot/Marketo
      - Mailchimp/SendGrid
      - Hootsuite/Buffer

  integration_points:
    - CRM sync
    - Analytics data
    - Lead scoring
    - Attribution tracking
```

### 10.3 Performance Monitoring **[REQUIRED]**

```yaml
monitoring:
  kpis:
    seo:
      - Organic traffic
      - Keyword rankings
      - Click-through rate
      - Conversion rate

    performance:
      - Page load time
      - Core Web Vitals
      - Server response time
      - Error rates

    marketing:
      - Lead generation
      - Cost per lead
      - ROI/ROAS
      - Customer lifetime value

  reporting:
    frequency:
      daily: "Traffic and conversions"
      weekly: "Rankings and performance"
      monthly: "Comprehensive review"
      quarterly: "Strategy adjustment"
```

---

## Quick Reference

### SEO Checklist
```yaml
critical_seo_elements:
  - [ ] Unique title tags (50-60 chars)
  - [ ] Meta descriptions (150-160 chars)
  - [ ] One H1 per page
  - [ ] XML sitemap submitted
  - [ ] Schema markup implemented
  - [ ] Mobile-friendly design
  - [ ] HTTPS enabled
  - [ ] Page speed < 3 seconds
```

### Marketing Automation Quick Start
```yaml
automation_basics:
  - [ ] Lead capture forms
  - [ ] Thank you pages
  - [ ] Welcome email series
  - [ ] Lead scoring model
  - [ ] Nurture campaigns
  - [ ] Analytics tracking
  - [ ] A/B testing plan
```

---

**Remember:** SEO and marketing standards evolve rapidly. Regularly review search engine guidelines, algorithm updates, and industry best practices to maintain optimal performance.

## Implementation

### Getting Started

1. Review the relevant sections of this standard for your use case
2. Identify which guidelines apply to your project
3. Implement the required practices and patterns
4. Validate compliance using the provided checklists

### Implementation Checklist

- [ ] Review and understand applicable standards
- [ ] Implement required practices
- [ ] Follow recommended patterns
- [ ] Validate implementation against guidelines
- [ ] Document any deviations with justification
