# Content Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** CONT

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Content Strategy and Governance](#1-content-strategy-and-governance)
2. [Writing Guidelines](#2-writing-guidelines)
3. [Tone and Voice](#3-tone-and-voice)
4. [Content Types and Formats](#4-content-types-and-formats)
5. [Editorial Standards](#5-editorial-standards)
6. [Localization and Internationalization](#6-localization-and-internationalization)
7. [SEO and Content Optimization](#7-seo-and-content-optimization)
8. [Content Management and Workflow](#8-content-management-and-workflow)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Content Strategy and Governance

### 1.1 Content Strategy Framework

#### Strategic Foundation **[REQUIRED]**
```yaml
# content-strategy.yaml
content_strategy:
  mission:
    statement: "Deliver clear, helpful, and accessible content that empowers users to succeed"
    alignment: "Business objectives and user needs"

  principles:
    clarity:
      description: "Write in plain language that anyone can understand"
      guidelines:
        - Use simple words and short sentences
        - Avoid jargon and technical terms when possible
        - Define complex concepts clearly
        - Lead with the most important information

    helpfulness:
      description: "Provide value in every piece of content"
      guidelines:
        - Answer real user questions
        - Offer actionable guidance
        - Include relevant examples
        - Link to additional resources

    accessibility:
      description: "Ensure content is usable by everyone"
      guidelines:
        - Write at an 8th-grade reading level
        - Use descriptive headings and links
        - Provide alt text for images
        - Structure content logically

    consistency:
      description: "Maintain unified voice and style"
      guidelines:
        - Follow established style guide
        - Use approved terminology
        - Apply consistent formatting
        - Maintain brand voice

  success_metrics:
    engagement:
      - Time on page
      - Scroll depth
      - Click-through rate
      - Social shares

    effectiveness:
      - Task completion rate
      - Support ticket reduction
      - User satisfaction score
      - Content helpfulness rating

    reach:
      - Page views
      - Unique visitors
      - Search rankings
      - Referral traffic
```

#### Content Governance Model **[REQUIRED]**
```yaml
# governance-model.yaml
governance_structure:
  roles:
    content_owner:
      responsibilities:
        - Define content strategy
        - Approve major changes
        - Allocate resources
        - Monitor performance

    content_manager:
      responsibilities:
        - Implement content strategy
        - Manage editorial calendar
        - Coordinate contributors
        - Ensure quality standards

    subject_matter_experts:
      responsibilities:
        - Provide technical accuracy
        - Review specialized content
        - Update domain knowledge
        - Validate information

    content_creators:
      responsibilities:
        - Write and edit content
        - Follow style guidelines
        - Meet deadlines
        - Incorporate feedback

    reviewers:
      responsibilities:
        - Check accuracy and clarity
        - Ensure compliance
        - Verify style adherence
        - Approve publication

  approval_workflow:
    levels:
      - draft: "Initial content creation"
      - review: "SME and editorial review"
      - legal: "Legal/compliance check (if needed)"
      - final: "Content manager approval"
      - publish: "Publication to production"

    sla:
      draft_to_review: "2 business days"
      review_to_approval: "3 business days"
      approval_to_publish: "1 business day"
```

### 1.2 Content Audit and Planning

#### Content Inventory Template **[REQUIRED]**
```typescript
// types/content-inventory.ts
interface ContentItem {
  id: string;
  title: string;
  url: string;
  type: ContentType;
  format: ContentFormat;
  owner: string;
  created: Date;
  lastUpdated: Date;
  lastReviewed: Date;
  nextReview: Date;
  status: ContentStatus;
  metrics: ContentMetrics;
  metadata: ContentMetadata;
}

enum ContentType {
  Article = 'article',
  Tutorial = 'tutorial',
  Reference = 'reference',
  FAQ = 'faq',
  Video = 'video',
  Infographic = 'infographic',
  CaseStudy = 'case-study',
  Whitepaper = 'whitepaper',
  Email = 'email',
  SocialPost = 'social-post'
}

enum ContentStatus {
  Draft = 'draft',
  InReview = 'in-review',
  Approved = 'approved',
  Published = 'published',
  Archived = 'archived',
  Outdated = 'outdated'
}

interface ContentMetrics {
  pageViews: number;
  uniqueVisitors: number;
  avgTimeOnPage: number;
  bounceRate: number;
  conversionRate: number;
  satisfactionScore?: number;
}

interface ContentMetadata {
  keywords: string[];
  category: string;
  tags: string[];
  audience: string[];
  relatedContent: string[];
  seoScore?: number;
  readabilityScore?: number;
}
```

#### Editorial Calendar **[REQUIRED]**
```typescript
// components/EditorialCalendar.tsx
interface EditorialCalendarEntry {
  id: string;
  title: string;
  type: ContentType;
  author: string;
  assignedTo: string;
  status: ContentStatus;
  dueDate: Date;
  publishDate?: Date;
  campaign?: string;
  channel: PublishingChannel[];
  priority: Priority;
  notes: string;
}

enum PublishingChannel {
  Website = 'website',
  Blog = 'blog',
  Email = 'email',
  Social = 'social',
  Newsletter = 'newsletter',
  Documentation = 'documentation'
}

enum Priority {
  Urgent = 'urgent',
  High = 'high',
  Medium = 'medium',
  Low = 'low'
}

// Editorial calendar configuration
const editorialConfig = {
  planning_horizon: '3 months',
  review_cycle: 'weekly',
  content_mix: {
    educational: 40,
    product: 30,
    thought_leadership: 20,
    community: 10
  },
  publishing_frequency: {
    blog: 'twice weekly',
    social: 'daily',
    email: 'weekly',
    documentation: 'as needed'
  }
};
```

---

## 2. Writing Guidelines

### 2.1 Grammar and Style

#### Writing Principles **[REQUIRED]**
```yaml
# writing-principles.yaml
grammar_standards:
  sentence_structure:
    preferred:
      - Active voice
      - Present tense
      - Simple sentences
      - Parallel construction

    avoid:
      - Passive voice (except when necessary)
      - Complex subordinate clauses
      - Double negatives
      - Ambiguous pronouns

  word_choice:
    use:
      - Common, everyday words
      - Concrete nouns
      - Strong verbs
      - Specific descriptions

    avoid:
      - Jargon without explanation
      - Buzzwords and clichés
      - Redundant phrases
      - Vague modifiers

punctuation_rules:
  oxford_comma: required
  quotation_marks: "Use double quotes for speech, single for quotes within quotes"
  hyphens_and_dashes:
    hyphen: "Compound words (e-commerce)"
    en_dash: "Ranges (10–15 minutes)"
    em_dash: "Emphasis—like this"

  lists:
    bulleted:
      - Use for unordered items
      - Capitalize first word
      - Use periods for complete sentences
      - Maintain parallel structure

    numbered:
      - Use for sequential steps
      - Use for ranked items
      - Capitalize first word
      - Include periods
```

#### Common Style Decisions **[REQUIRED]**
```yaml
# style-decisions.yaml
formatting:
  capitalization:
    - Sentence case for headings
    - Title case for proper nouns only
    - lowercase for email addresses and URLs

  numbers:
    - Spell out one through nine
    - Use numerals for 10 and above
    - Always use numerals for percentages (5%)
    - Use numerals for ages, measurements, and money

  dates_and_times:
    - Month DD, YYYY (January 15, 2025)
    - 12-hour clock with AM/PM
    - Time zones in parentheses (2 PM EST)
    - Use "to" not dashes for ranges

  abbreviations:
    - Spell out on first use
    - Include abbreviation in parentheses
    - Common exceptions: URL, API, FAQ
    - Avoid Latin abbreviations (use "for example" not "e.g.")

technical_writing:
  code_references:
    - Use backticks for inline code
    - Use code blocks for multi-line examples
    - Include language identifier
    - Provide context and explanation

  ui_elements:
    - Bold for button names: Click **Save**
    - Use quotation marks for field labels
    - Describe location when helpful
    - Include screenshots for complex tasks
```

### 2.2 Content Structure

#### Information Architecture **[REQUIRED]**
```markdown
# Document Structure Template

## Title (H1)
- Clear, descriptive, and keyword-rich
- Maximum 60 characters for SEO
- Accurately represents content

### Introduction
- Hook: Grab attention in first sentence
- Context: Why this matters to the reader
- Value proposition: What they'll learn
- Overview: Brief outline of content

### Body Sections (H2)
#### Subsections (H3)
- One main idea per section
- Logical flow between sections
- Progressive disclosure of information
- Clear transitions

##### Supporting Points (H4)
- Examples and evidence
- Data and statistics
- Expert quotes
- Case studies

### Conclusion
- Summary of key points
- Call to action
- Next steps
- Related resources

## Content Patterns

### For How-To Articles
1. **Problem Statement**: What issue does this solve?
2. **Prerequisites**: What's needed before starting
3. **Step-by-Step Instructions**: Numbered, actionable steps
4. **Troubleshooting**: Common issues and solutions
5. **Summary**: What was accomplished

### For Conceptual Content
1. **Definition**: What is this concept?
2. **Why It Matters**: Business value and use cases
3. **How It Works**: Technical explanation
4. **Examples**: Real-world applications
5. **Best Practices**: Implementation guidance

### For Reference Documentation
1. **Overview**: Purpose and scope
2. **Syntax/Parameters**: Technical details
3. **Examples**: Code samples with explanation
4. **Related Topics**: Links to connected content
5. **Version Notes**: Changes and updates
```

#### Scannable Content **[REQUIRED]**
```scss
// styles/content-typography.scss
// Making content scannable and readable

.content {
  // Optimal line length for reading
  max-width: 65ch;

  // Paragraph spacing
  p {
    margin-bottom: 1.5em;
    line-height: 1.6;
  }

  // Heading hierarchy
  h2 {
    margin-top: 2em;
    margin-bottom: 0.5em;
    font-size: 1.75em;
  }

  h3 {
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-size: 1.25em;
  }

  // Lists for scannability
  ul, ol {
    margin: 1em 0;
    padding-left: 2em;

    li {
      margin-bottom: 0.5em;
    }
  }

  // Callout boxes
  .callout {
    margin: 2em 0;
    padding: 1em;
    border-left: 4px solid;
    background-color: var(--callout-bg);

    &--tip {
      border-color: var(--color-success);
    }

    &--warning {
      border-color: var(--color-warning);
    }

    &--info {
      border-color: var(--color-info);
    }
  }

  // Pull quotes
  .pull-quote {
    margin: 2em 0;
    padding: 0 2em;
    font-size: 1.25em;
    font-style: italic;
    text-align: center;
    color: var(--color-secondary);
  }
}
```

---

## 3. Tone and Voice

### 3.1 Brand Voice Definition

#### Voice Attributes **[REQUIRED]**
```yaml
# brand-voice.yaml
brand_voice:
  personality_traits:
    primary:
      friendly:
        description: "Warm and approachable, never cold or robotic"
        examples:
          do: "We're here to help you succeed"
          dont: "Users must complete the following steps"

      clear:
        description: "Direct and easy to understand"
        examples:
          do: "Click Save to keep your changes"
          dont: "Actuate the preservation mechanism to persist modifications"

      confident:
        description: "Knowledgeable without being arrogant"
        examples:
          do: "This method improves performance by 50%"
          dont: "This might possibly help performance"

    secondary:
      helpful:
        description: "Focused on user success"
        techniques:
          - Anticipate user needs
          - Provide context
          - Offer solutions
          - Include examples

      human:
        description: "Conversational and relatable"
        techniques:
          - Use contractions (we're, you'll)
          - Address reader directly
          - Acknowledge challenges
          - Celebrate successes

  voice_spectrum:
    formality: "Professional but conversational"
    humor: "Light and occasional, never forced"
    emotion: "Empathetic and encouraging"
    technicality: "Accessible, with technical depth when needed"
```

#### Tone Variations **[REQUIRED]**
```yaml
# tone-variations.yaml
situational_tone:
  success_messages:
    tone: "Celebratory and encouraging"
    examples:
      - "Great job! Your project is now live."
      - "Success! Your data has been saved."
      - "You're all set! Here's what happens next..."

  error_messages:
    tone: "Calm, helpful, and solution-focused"
    examples:
      - "Something went wrong, but we can fix it."
      - "We couldn't process that request. Here's why..."
      - "Let's try a different approach."

  educational_content:
    tone: "Patient and encouraging"
    examples:
      - "Let's explore how this works..."
      - "Don't worry if this seems complex at first."
      - "You'll master this in no time."

  marketing_content:
    tone: "Inspiring and benefit-focused"
    examples:
      - "Imagine what you could build..."
      - "Join thousands who've transformed their workflow."
      - "Start creating something amazing today."

  technical_documentation:
    tone: "Precise and instructive"
    examples:
      - "This function returns a Promise that resolves..."
      - "Configure the following parameters..."
      - "The API expects a JSON payload with..."
```

### 3.2 Writing for Different Audiences

#### Audience Personas **[REQUIRED]**
```typescript
// types/audience-personas.ts
interface AudiencePersona {
  id: string;
  name: string;
  description: string;
  technicalLevel: 'beginner' | 'intermediate' | 'advanced';
  goals: string[];
  painPoints: string[];
  preferredContent: ContentType[];
  vocabulary: VocabularyLevel;
  readingContext: ReadingContext;
}

interface VocabularyLevel {
  technicalTerms: 'avoid' | 'explain' | 'use-freely';
  industryJargon: 'avoid' | 'explain' | 'use-freely';
  codeExamples: 'minimal' | 'moderate' | 'extensive';
}

interface ReadingContext {
  timeAvailable: 'limited' | 'moderate' | 'extensive';
  device: ('desktop' | 'mobile' | 'tablet')[];
  environment: ('office' | 'home' | 'commute')[];
}

// Example personas
const personas: AudiencePersona[] = [
  {
    id: 'dev-beginner',
    name: 'New Developer',
    description: 'Learning to code, needs fundamentals',
    technicalLevel: 'beginner',
    goals: ['Learn basics', 'Build first project', 'Understand concepts'],
    painPoints: ['Overwhelming terminology', 'Complex examples', 'Lack of context'],
    preferredContent: [ContentType.Tutorial, ContentType.Video],
    vocabulary: {
      technicalTerms: 'explain',
      industryJargon: 'avoid',
      codeExamples: 'minimal'
    },
    readingContext: {
      timeAvailable: 'extensive',
      device: ['desktop', 'tablet'],
      environment: ['home', 'office']
    }
  },
  {
    id: 'dev-senior',
    name: 'Senior Developer',
    description: 'Experienced, needs advanced topics',
    technicalLevel: 'advanced',
    goals: ['Optimize performance', 'Learn best practices', 'Stay updated'],
    painPoints: ['Basic explanations', 'Lack of depth', 'Outdated information'],
    preferredContent: [ContentType.Reference, ContentType.Whitepaper],
    vocabulary: {
      technicalTerms: 'use-freely',
      industryJargon: 'use-freely',
      codeExamples: 'extensive'
    },
    readingContext: {
      timeAvailable: 'limited',
      device: ['desktop'],
      environment: ['office']
    }
  }
];
```

#### Adaptive Writing **[RECOMMENDED]**
```typescript
// utils/content-adapter.ts
class ContentAdapter {
  adaptContent(
    content: string,
    persona: AudiencePersona
  ): AdaptedContent {
    return {
      content: this.adjustComplexity(content, persona),
      readingTime: this.calculateReadingTime(content, persona),
      summaryLength: this.determineSummaryLength(persona),
      codeExampleDepth: this.determineCodeDepth(persona),
      visualAids: this.suggestVisuals(content, persona)
    };
  }

  private adjustComplexity(
    content: string,
    persona: AudiencePersona
  ): string {
    if (persona.technicalLevel === 'beginner') {
      return this.simplifyLanguage(content);
    } else if (persona.technicalLevel === 'advanced') {
      return this.addTechnicalDepth(content);
    }
    return content;
  }

  private simplifyLanguage(content: string): string {
    // Replace complex terms with simpler alternatives
    const replacements = {
      'instantiate': 'create',
      'parameter': 'input',
      'asynchronous': 'non-blocking',
      'repository': 'project folder',
      'dependency': 'required package'
    };

    let simplified = content;
    Object.entries(replacements).forEach(([complex, simple]) => {
      simplified = simplified.replace(
        new RegExp(complex, 'gi'),
        simple
      );
    });

    return simplified;
  }
}
```

---

## 4. Content Types and Formats

### 4.1 Documentation Types

#### Technical Documentation **[REQUIRED]**
```markdown
# Technical Documentation Template

## API Reference Template

### Endpoint Name

**Description**: Brief explanation of what this endpoint does

**Method**: `GET | POST | PUT | DELETE`

**URL**: `/api/v1/resource/{id}`

**Authentication**: Required | Optional

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Unique identifier |
| filter | string | No | Filter results |

#### Request Body

```json
{
  "field1": "string",
  "field2": 123,
  "field3": {
    "nested": "value"
  }
}
```

#### Response

**Success Response (200 OK)**
```json
{
  "status": "success",
  "data": {
    "id": "123",
    "field1": "value"
  }
}
```

**Error Response (400 Bad Request)**
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_INPUT",
    "message": "Field validation failed"
  }
}
```

#### Example Usage

```bash
curl -X GET "https://api.example.com/v1/resource/123" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

#### Notes
- Rate limit: 100 requests per minute
- Pagination: Use `page` and `limit` parameters
- Filtering: Supports partial matches
```

#### User Documentation **[REQUIRED]**
```markdown
# User Guide Template

## Feature Name

### What You'll Learn
- Clear learning objectives
- Expected outcomes
- Time to complete

### Before You Begin
- Prerequisites
- Required access/permissions
- System requirements

### Step-by-Step Instructions

1. **First Step Title**

   Description of what to do.

   ![Screenshot with annotations](image-url)

   > **Tip**: Helpful information or shortcut

2. **Second Step Title**

   More detailed instructions with:
   - Sub-steps if needed
   - Clear action verbs
   - Expected results

   > **Note**: Important information to remember

### Troubleshooting

**Problem**: Common issue description
**Solution**: Step-by-step fix

**Problem**: Another common issue
**Solution**: Alternative approach

### Next Steps
- Related features to explore
- Advanced configurations
- Additional resources
```

### 4.2 Marketing Content

#### Blog Post Structure **[REQUIRED]**
```yaml
# blog-post-template.yaml
blog_structure:
  headline:
    requirements:
      - Maximum 60 characters
      - Include primary keyword
      - Create curiosity or promise value
      - Use numbers when applicable

    formulas:
      - "How to [Achieve Desired Outcome] in [Time Period]"
      - "[Number] Ways to [Solve Problem]"
      - "The Complete Guide to [Topic]"
      - "Why [Conventional Wisdom] Is Wrong"

  introduction:
    elements:
      - Hook (question, statistic, or story)
      - Problem identification
      - Solution preview
      - Article roadmap

    length: "100-150 words"

  body:
    structure:
      - Use subheadings every 300 words
      - Include examples and data
      - Add visuals every 500 words
      - Use bullet points for lists

    elements:
      - Supporting arguments
      - Case studies
      - Expert quotes
      - Data visualizations

  conclusion:
    elements:
      - Key takeaways summary
      - Call to action
      - Related resources
      - Comments invitation

    length: "75-100 words"

  seo_checklist:
    - Primary keyword in title
    - Keywords in first 100 words
    - Keywords in subheadings
    - Alt text for images
    - Meta description (155 chars)
    - Internal and external links
```

#### Email Templates **[REQUIRED]**
```html
<!-- email-template.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ subject_line }}</title>
  <style>
    /* Email-safe CSS */
    body {
      font-family: -apple-system, Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
    }

    .header {
      text-align: center;
      padding: 20px 0;
      border-bottom: 2px solid #eee;
    }

    .content {
      padding: 30px 0;
    }

    .cta-button {
      display: inline-block;
      padding: 12px 30px;
      background-color: #007bff;
      color: white;
      text-decoration: none;
      border-radius: 5px;
      margin: 20px 0;
    }

    .footer {
      padding-top: 30px;
      border-top: 2px solid #eee;
      text-align: center;
      font-size: 14px;
      color: #666;
    }
  </style>
</head>
<body>
  <!-- Preheader Text -->
  <div style="display:none;font-size:1px;color:#333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    {{ preheader_text }}
  </div>

  <!-- Header -->
  <div class="header">
    <img src="{{ logo_url }}" alt="{{ company_name }}" width="200">
  </div>

  <!-- Main Content -->
  <div class="content">
    <h1>{{ headline }}</h1>

    <p>Hi {{ first_name }},</p>

    <p>{{ opening_paragraph }}</p>

    <!-- Body Content -->
    {{ body_content }}

    <!-- Call to Action -->
    <div style="text-align: center;">
      <a href="{{ cta_url }}" class="cta-button">{{ cta_text }}</a>
    </div>

    <p>{{ closing_paragraph }}</p>

    <p>Best regards,<br>
    {{ sender_name }}<br>
    {{ sender_title }}</p>
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>{{ company_address }}</p>
    <p>
      <a href="{{ unsubscribe_url }}">Unsubscribe</a> |
      <a href="{{ preferences_url }}">Update Preferences</a>
    </p>
  </div>
</body>
</html>
```

### 4.3 Social Media Content

#### Platform-Specific Guidelines **[REQUIRED]**
```yaml
# social-media-guidelines.yaml
platform_guidelines:
  twitter:
    character_limit: 280
    optimal_length: "100-150 characters"
    hashtags: "1-2 per tweet"
    media: "Images, GIFs, videos (2:20 max)"
    best_practices:
      - Lead with the hook
      - Use threads for complex topics
      - Include visuals when possible
      - Engage with replies

    content_types:
      - Quick tips
      - Industry news commentary
      - Thread tutorials
      - Polls and questions

  linkedin:
    character_limit: 3000
    optimal_length: "150-300 characters"
    hashtags: "3-5 per post"
    media: "Images, videos, documents"
    best_practices:
      - Professional tone
      - Industry insights
      - Thought leadership
      - Career advice

    content_types:
      - Article shares with commentary
      - Industry analysis
      - Company updates
      - Professional achievements

  instagram:
    caption_limit: 2200
    optimal_length: "138-150 characters"
    hashtags: "10-30 per post"
    media: "Images, videos (60s feed, 15s stories)"
    best_practices:
      - Visual-first content
      - Stories for behind-scenes
      - Consistent aesthetic
      - User-generated content

    content_types:
      - Product showcases
      - Behind the scenes
      - User testimonials
      - Educational carousels
```

#### Content Calendar Integration **[REQUIRED]**
```typescript
// utils/social-scheduler.ts
interface SocialPost {
  id: string;
  platform: SocialPlatform[];
  content: PlatformContent[];
  media?: MediaAsset[];
  publishTime: Date;
  campaign?: string;
  status: PostStatus;
  performance?: PostMetrics;
}

interface PlatformContent {
  platform: SocialPlatform;
  text: string;
  hashtags: string[];
  mentions?: string[];
  link?: string;
}

interface MediaAsset {
  type: 'image' | 'video' | 'gif';
  url: string;
  altText: string;
  dimensions: {
    width: number;
    height: number;
  };
}

interface PostMetrics {
  impressions: number;
  engagements: number;
  clicks: number;
  shares: number;
  comments: number;
  sentiment?: 'positive' | 'neutral' | 'negative';
}

class SocialContentOptimizer {
  optimizeForPlatform(
    content: string,
    platform: SocialPlatform
  ): PlatformContent {
    const rules = this.getPlatformRules(platform);

    return {
      platform,
      text: this.truncateText(content, rules.characterLimit),
      hashtags: this.selectHashtags(content, rules.hashtagLimit),
      mentions: this.extractMentions(content),
      link: this.extractLink(content)
    };
  }

  private getPlatformRules(platform: SocialPlatform) {
    const rules = {
      twitter: {
        characterLimit: 280,
        hashtagLimit: 2,
        mediaTypes: ['image', 'gif', 'video']
      },
      linkedin: {
        characterLimit: 3000,
        hashtagLimit: 5,
        mediaTypes: ['image', 'video', 'document']
      },
      instagram: {
        characterLimit: 2200,
        hashtagLimit: 30,
        mediaTypes: ['image', 'video']
      }
    };

    return rules[platform];
  }
}
```

---

## 5. Editorial Standards

### 5.1 Fact-Checking and Accuracy

#### Verification Process **[REQUIRED]**
```yaml
# fact-checking-process.yaml
verification_standards:
  information_sources:
    primary:
      - Original research
      - Official documentation
      - Direct interviews
      - Company data

    secondary:
      - Peer-reviewed journals
      - Reputable news sources
      - Industry reports
      - Government statistics

    unacceptable:
      - Wikipedia as sole source
      - Unverified social media
      - Anonymous sources
      - Outdated information (>2 years)

  verification_steps:
    1_identify:
      action: "Identify all claims requiring verification"
      includes:
        - Statistics and data
        - Technical specifications
        - Quotes and attributions
        - Historical facts

    2_source:
      action: "Find authoritative sources"
      requirements:
        - Minimum two sources for facts
        - Primary source preferred
        - Recent and relevant
        - Credible authority

    3_verify:
      action: "Cross-check information"
      methods:
        - Compare multiple sources
        - Contact subject matter experts
        - Review official documentation
        - Check for updates or corrections

    4_document:
      action: "Record verification"
      includes:
        - Source citations
        - Verification date
        - Reviewer name
        - Confidence level

  citation_format:
    inline: "[Source Name](url)"
    footnote: "^1 Source Name, Publication, Date"
    bibliography: "Author. (Year). Title. Publisher. URL"
```

#### Quality Checklist **[REQUIRED]**
```typescript
// types/editorial-checklist.ts
interface EditorialChecklist {
  content: ContentChecks;
  technical: TechnicalChecks;
  legal: LegalChecks;
  seo: SEOChecks;
  accessibility: AccessibilityChecks;
}

interface ContentChecks {
  accuracy: boolean;
  clarity: boolean;
  completeness: boolean;
  tone_appropriate: boolean;
  grammar_correct: boolean;
  style_compliant: boolean;
  sources_verified: boolean;
  facts_checked: boolean;
}

interface TechnicalChecks {
  code_tested: boolean;
  examples_working: boolean;
  links_valid: boolean;
  images_optimized: boolean;
  formatting_correct: boolean;
}

interface LegalChecks {
  copyright_cleared: boolean;
  trademarks_appropriate: boolean;
  claims_substantiated: boolean;
  disclaimers_included: boolean;
  gdpr_compliant: boolean;
}

// Automated quality checks
class QualityAnalyzer {
  async analyzeContent(content: string): Promise<QualityReport> {
    const report: QualityReport = {
      readability: await this.checkReadability(content),
      grammar: await this.checkGrammar(content),
      spelling: await this.checkSpelling(content),
      links: await this.validateLinks(content),
      seo: await this.analyzeSEO(content),
      inclusivity: await this.checkInclusivity(content)
    };

    return report;
  }

  private async checkReadability(content: string): Promise<ReadabilityScore> {
    // Flesch-Kincaid Grade Level
    const sentences = content.split(/[.!?]+/).length;
    const words = content.split(/\s+/).length;
    const syllables = this.countSyllables(content);

    const score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words);
    const gradeLevel = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59;

    return {
      fleschScore: score,
      gradeLevel: gradeLevel,
      rating: this.getReadabilityRating(score)
    };
  }
}
```

### 5.2 Editorial Workflow

#### Review Process **[REQUIRED]**
```yaml
# editorial-workflow.yaml
review_stages:
  1_self_review:
    owner: "Content creator"
    duration: "30 minutes"
    checklist:
      - Spelling and grammar
      - Style guide compliance
      - Link validation
      - Image optimization
      - Meta information

  2_peer_review:
    owner: "Team member"
    duration: "1 hour"
    checklist:
      - Content clarity
      - Technical accuracy
      - Tone consistency
      - Structure and flow
      - Target audience fit

  3_sme_review:
    owner: "Subject matter expert"
    duration: "2 hours"
    checklist:
      - Technical correctness
      - Completeness
      - Best practices
      - Industry standards
      - Updated information

  4_editorial_review:
    owner: "Editor"
    duration: "1 hour"
    checklist:
      - Brand voice
      - Style consistency
      - Legal compliance
      - SEO optimization
      - Publishing readiness

  5_final_approval:
    owner: "Content manager"
    duration: "30 minutes"
    checklist:
      - Strategic alignment
      - Quality standards
      - Publishing schedule
      - Cross-references
      - Campaign coordination

feedback_guidelines:
  constructive:
    - Be specific about issues
    - Suggest improvements
    - Explain the why
    - Prioritize changes

  collaborative:
    - Ask questions
    - Discuss alternatives
    - Respect expertise
    - Find solutions together
```

#### Version Control **[REQUIRED]**
```typescript
// utils/content-versioning.ts
interface ContentVersion {
  id: string;
  contentId: string;
  version: string;
  author: string;
  timestamp: Date;
  changes: ContentChange[];
  status: VersionStatus;
  reviewers: Reviewer[];
  publishedDate?: Date;
}

interface ContentChange {
  type: 'addition' | 'deletion' | 'modification';
  section: string;
  before?: string;
  after?: string;
  reason: string;
}

interface Reviewer {
  name: string;
  role: ReviewerRole;
  reviewDate: Date;
  status: 'approved' | 'rejected' | 'pending';
  comments?: string;
}

enum VersionStatus {
  Draft = 'draft',
  InReview = 'in-review',
  Approved = 'approved',
  Published = 'published',
  Archived = 'archived'
}

class ContentVersionManager {
  createVersion(
    content: Content,
    changes: ContentChange[]
  ): ContentVersion {
    const previousVersion = this.getLatestVersion(content.id);
    const newVersionNumber = this.incrementVersion(previousVersion.version);

    return {
      id: generateId(),
      contentId: content.id,
      version: newVersionNumber,
      author: getCurrentUser(),
      timestamp: new Date(),
      changes: changes,
      status: VersionStatus.Draft,
      reviewers: []
    };
  }

  private incrementVersion(version: string): string {
    const [major, minor, patch] = version.split('.').map(Number);

    // Increment based on change type
    if (this.isMajorChange()) {
      return `${major + 1}.0.0`;
    } else if (this.isMinorChange()) {
      return `${major}.${minor + 1}.0`;
    } else {
      return `${major}.${minor}.${patch + 1}`;
    }
  }
}
```

---

## 6. Localization and Internationalization

### 6.1 Localization Strategy

#### Language Guidelines **[REQUIRED]**
```yaml
# localization-strategy.yaml
localization_approach:
  supported_languages:
    tier_1:
      - en-US (English - United States) # Primary
      - es-ES (Spanish - Spain)
      - fr-FR (French - France)
      - de-DE (German - Germany)
      - ja-JP (Japanese - Japan)

    tier_2:
      - pt-BR (Portuguese - Brazil)
      - it-IT (Italian - Italy)
      - ko-KR (Korean - South Korea)
      - zh-CN (Chinese - Simplified)
      - nl-NL (Dutch - Netherlands)

  content_priorities:
    high:
      - User interface strings
      - Error messages
      - Core documentation
      - Legal content

    medium:
      - Marketing content
      - Blog posts
      - Help articles
      - Email templates

    low:
      - Social media
      - Internal documentation
      - Technical specifications

translation_guidelines:
  quality_standards:
    - Native speaker translators required
    - Industry expertise preferred
    - Consistency with glossary mandatory
    - Cultural adaptation encouraged

  tone_adaptation:
    formal_languages: [ja-JP, de-DE, fr-FR]
    informal_languages: [en-US, pt-BR]
    context_dependent: [es-ES, it-IT]

  review_process:
    - Initial translation
    - In-context review
    - Native speaker validation
    - Technical accuracy check
    - Final proofreading
```

#### Translation Management **[REQUIRED]**
```typescript
// i18n/translation-manager.ts
interface TranslationProject {
  id: string;
  sourceLanguage: string;
  targetLanguages: string[];
  content: TranslatableContent[];
  deadline: Date;
  status: TranslationStatus;
  quality: QualityMetrics;
}

interface TranslatableContent {
  id: string;
  key: string;
  source: string;
  context?: string;
  maxLength?: number;
  translations: Translation[];
  metadata: TranslationMetadata;
}

interface Translation {
  language: string;
  value: string;
  translator: string;
  reviewedBy?: string;
  status: 'pending' | 'translated' | 'reviewed' | 'approved';
  quality?: number;
  notes?: string;
}

interface TranslationMetadata {
  contentType: 'ui' | 'documentation' | 'marketing' | 'legal';
  lastUpdated: Date;
  characterCount: number;
  wordCount: number;
  placeholders?: string[];
  terminology?: string[];
}

// Localization utilities
class LocalizationUtils {
  // Format numbers according to locale
  formatNumber(value: number, locale: string): string {
    return new Intl.NumberFormat(locale).format(value);
  }

  // Format dates according to locale
  formatDate(date: Date, locale: string, format: 'short' | 'long'): string {
    const options: Intl.DateTimeFormatOptions =
      format === 'short'
        ? { year: 'numeric', month: 'short', day: 'numeric' }
        : { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

    return new Intl.DateTimeFormat(locale, options).format(date);
  }

  // Handle pluralization rules
  pluralize(count: number, locale: string, forms: Record<string, string>): string {
    const pr = new Intl.PluralRules(locale);
    const rule = pr.select(count);
    return forms[rule] || forms.other;
  }
}
```

### 6.2 Cultural Adaptation

#### Cultural Considerations **[REQUIRED]**
```yaml
# cultural-adaptation.yaml
cultural_guidelines:
  imagery:
    considerations:
      - Representation and diversity
      - Cultural symbols and meanings
      - Color associations
      - Gesture appropriateness
      - Religious sensitivity

    regional_preferences:
      western:
        - Individual achievement
        - Direct communication
        - Innovation focus

      eastern:
        - Group harmony
        - Indirect communication
        - Tradition respect

  content_adaptation:
    examples_and_references:
      localize:
        - Pop culture references
        - Sports analogies
        - Historical events
        - Currency and units
        - Business practices

      maintain:
        - Technical specifications
        - Product names
        - Brand terminology
        - Industry standards

    communication_style:
      high_context_cultures: [ja-JP, ko-KR, zh-CN]
        - More formal tone
        - Indirect messaging
        - Relationship building

      low_context_cultures: [en-US, de-DE, nl-NL]
        - Direct communication
        - Explicit information
        - Task focused

  legal_requirements:
    gdpr_regions: [EU countries]
    ccpa_regions: [California, USA]
    accessibility_standards:
      - WCAG 2.1 AA (Global)
      - Section 508 (USA)
      - EN 301 549 (EU)
      - JIS X 8341 (Japan)
```

#### Right-to-Left Support **[REQUIRED]**
```scss
// styles/rtl-support.scss
// Bidirectional text support

[dir="rtl"] {
  // Text alignment
  text-align: right;

  // Layout mirroring
  .container {
    direction: rtl;
  }

  // Spacing adjustments
  .content {
    padding-left: 0;
    padding-right: 20px;

    ul, ol {
      padding-right: 40px;
      padding-left: 0;
    }
  }

  // Component mirroring
  .nav-menu {
    flex-direction: row-reverse;

    &__icon {
      margin-right: 0;
      margin-left: 8px;
    }
  }

  // Form elements
  .form-field {
    &__label {
      text-align: right;
    }

    &__input {
      text-align: right;

      &[type="email"],
      &[type="url"],
      &[type="number"] {
        text-align: left;
        direction: ltr;
      }
    }
  }

  // Icons that need flipping
  .icon-arrow-right {
    transform: scaleX(-1);
  }
}

// Logical properties for automatic RTL support
.modern-layout {
  // Use logical properties instead of physical
  margin-inline-start: 20px; // Instead of margin-left
  padding-inline-end: 10px; // Instead of padding-right
  border-inline-start: 2px solid; // Instead of border-left

  // Logical values
  text-align: start; // Instead of left
  float: inline-start; // Instead of float: left
}
```

---

## 7. SEO and Content Optimization

### 7.1 SEO Best Practices

#### On-Page Optimization **[REQUIRED]**
```yaml
# seo-optimization.yaml
on_page_elements:
  title_tags:
    requirements:
      - Unique for each page
      - 50-60 characters maximum
      - Include primary keyword
      - Brand name at end

    format: "[Primary Keyword] - [Secondary Info] | [Brand]"

  meta_descriptions:
    requirements:
      - 150-160 characters maximum
      - Include primary keyword
      - Compelling call to action
      - Unique for each page

    format: "Action-oriented description with keyword and value proposition."

  heading_structure:
    h1:
      - One per page
      - Include primary keyword
      - Match search intent
      - 20-70 characters

    h2_h3:
      - Support main topic
      - Include related keywords
      - Create content hierarchy
      - Improve scannability

  url_structure:
    guidelines:
      - Use hyphens not underscores
      - Include target keyword
      - Keep under 60 characters
      - Remove stop words
      - Use lowercase only

    examples:
      good: "/blog/content-marketing-strategy"
      bad: "/blog/post_12345_final_v2"

keyword_optimization:
  research:
    tools:
      - Google Keyword Planner
      - SEMrush
      - Ahrefs
      - Google Search Console

    criteria:
      - Search volume > 100/month
      - Keyword difficulty < 70
      - Business relevance: high
      - Search intent match

  placement:
    primary_keyword:
      - Title tag
      - H1 heading
      - First paragraph
      - URL slug
      - Meta description
      - 2-3 times in body

    secondary_keywords:
      - H2/H3 headings
      - Throughout body naturally
      - Image alt text
      - Related content links
```

#### Technical SEO **[REQUIRED]**
```typescript
// utils/seo-analyzer.ts
interface SEOAnalysis {
  score: number;
  issues: SEOIssue[];
  recommendations: SEORecommendation[];
  metadata: PageMetadata;
}

interface SEOIssue {
  type: 'error' | 'warning' | 'info';
  category: SEOCategory;
  message: string;
  impact: 'high' | 'medium' | 'low';
  element?: string;
}

enum SEOCategory {
  Title = 'title',
  Meta = 'meta',
  Headings = 'headings',
  Content = 'content',
  Images = 'images',
  Links = 'links',
  Performance = 'performance',
  Mobile = 'mobile',
  Structured = 'structured-data'
}

class SEOAnalyzer {
  async analyzePage(url: string): Promise<SEOAnalysis> {
    const page = await this.fetchPage(url);
    const analysis: SEOAnalysis = {
      score: 0,
      issues: [],
      recommendations: [],
      metadata: this.extractMetadata(page)
    };

    // Check title
    this.analyzeTitle(page, analysis);

    // Check meta description
    this.analyzeMetaDescription(page, analysis);

    // Check headings
    this.analyzeHeadings(page, analysis);

    // Check content
    this.analyzeContent(page, analysis);

    // Check images
    this.analyzeImages(page, analysis);

    // Check performance
    await this.analyzePerformance(url, analysis);

    // Calculate score
    analysis.score = this.calculateScore(analysis);

    return analysis;
  }

  private analyzeTitle(page: Document, analysis: SEOAnalysis): void {
    const title = page.querySelector('title')?.textContent || '';

    if (!title) {
      analysis.issues.push({
        type: 'error',
        category: SEOCategory.Title,
        message: 'Missing title tag',
        impact: 'high'
      });
    } else {
      if (title.length > 60) {
        analysis.issues.push({
          type: 'warning',
          category: SEOCategory.Title,
          message: `Title too long: ${title.length} characters (max 60)`,
          impact: 'medium'
        });
      }

      if (title.length < 30) {
        analysis.issues.push({
          type: 'warning',
          category: SEOCategory.Title,
          message: `Title too short: ${title.length} characters (min 30)`,
          impact: 'medium'
        });
      }
    }
  }
}
```

### 7.2 Content Performance

#### Analytics Integration **[REQUIRED]**
```typescript
// analytics/content-tracking.ts
interface ContentMetrics {
  pageViews: number;
  uniqueVisitors: number;
  avgTimeOnPage: number;
  bounceRate: number;
  scrollDepth: number;
  exitRate: number;
  socialShares: SocialMetrics;
  conversions: ConversionMetrics;
  engagement: EngagementMetrics;
}

interface SocialMetrics {
  facebook: number;
  twitter: number;
  linkedin: number;
  email: number;
  total: number;
}

interface ConversionMetrics {
  signups: number;
  downloads: number;
  purchases: number;
  customGoals: Record<string, number>;
}

interface EngagementMetrics {
  comments: number;
  likes: number;
  shares: number;
  bookmarks: number;
  readingProgress: number[];
}

class ContentAnalytics {
  trackContentPerformance(contentId: string): void {
    // Page view tracking
    this.analytics.track('page_view', {
      content_id: contentId,
      content_type: this.getContentType(contentId),
      author: this.getAuthor(contentId),
      publish_date: this.getPublishDate(contentId),
      category: this.getCategory(contentId),
      tags: this.getTags(contentId)
    });

    // Scroll depth tracking
    this.trackScrollDepth(contentId);

    // Time on page tracking
    this.trackTimeOnPage(contentId);

    // Engagement tracking
    this.trackEngagement(contentId);
  }

  private trackScrollDepth(contentId: string): void {
    const thresholds = [25, 50, 75, 100];
    const observed = new Set<number>();

    window.addEventListener('scroll', throttle(() => {
      const scrollPercentage = (window.scrollY + window.innerHeight) /
        document.documentElement.scrollHeight * 100;

      thresholds.forEach(threshold => {
        if (scrollPercentage >= threshold && !observed.has(threshold)) {
          observed.add(threshold);
          this.analytics.track('scroll_depth', {
            content_id: contentId,
            depth: threshold
          });
        }
      });
    }, 1000));
  }
}
```

#### A/B Testing **[RECOMMENDED]**
```typescript
// testing/content-experiments.ts
interface ContentExperiment {
  id: string;
  name: string;
  hypothesis: string;
  variants: ContentVariant[];
  metrics: string[];
  audience: AudienceSegment;
  duration: Duration;
  status: ExperimentStatus;
  results?: ExperimentResults;
}

interface ContentVariant {
  id: string;
  name: string;
  changes: VariantChange[];
  traffic: number; // Percentage
  performance?: VariantPerformance;
}

interface VariantChange {
  element: string;
  type: 'text' | 'color' | 'layout' | 'cta';
  original: string;
  modified: string;
}

class ContentExperimentRunner {
  async runExperiment(experiment: ContentExperiment): Promise<void> {
    // Validate experiment setup
    this.validateExperiment(experiment);

    // Assign users to variants
    const variant = this.assignVariant(experiment);

    // Apply variant changes
    await this.applyVariant(variant);

    // Track exposure
    this.trackExposure(experiment, variant);

    // Monitor metrics
    this.monitorMetrics(experiment, variant);
  }

  private assignVariant(experiment: ContentExperiment): ContentVariant {
    const random = Math.random() * 100;
    let cumulative = 0;

    for (const variant of experiment.variants) {
      cumulative += variant.traffic;
      if (random <= cumulative) {
        return variant;
      }
    }

    return experiment.variants[0]; // Fallback to control
  }

  calculateSignificance(
    control: VariantPerformance,
    variant: VariantPerformance
  ): number {
    // Calculate statistical significance using Chi-square test
    const controlConversions = control.conversions;
    const controlTotal = control.visitors;
    const variantConversions = variant.conversions;
    const variantTotal = variant.visitors;

    // Implementation of significance calculation
    return this.chiSquareTest(
      controlConversions,
      controlTotal,
      variantConversions,
      variantTotal
    );
  }
}
```

---

## 8. Content Management and Workflow

### 8.1 Content Lifecycle

#### Content Planning **[REQUIRED]**
```yaml
# content-lifecycle.yaml
content_stages:
  1_ideation:
    activities:
      - Topic research
      - Keyword analysis
      - Audience needs assessment
      - Competitive analysis

    deliverables:
      - Content brief
      - Target keywords
      - Success metrics
      - Timeline

    tools:
      - Content calendar
      - Keyword research tools
      - Analytics dashboards
      - Competitor monitoring

  2_creation:
    activities:
      - Research and outline
      - First draft writing
      - Media creation
      - Internal review

    deliverables:
      - Complete draft
      - Supporting media
      - Meta information
      - Internal feedback

    quality_checks:
      - Accuracy verification
      - Style guide compliance
      - SEO optimization
      - Readability score

  3_review:
    activities:
      - Peer review
      - SME validation
      - Legal check
      - Final editing

    deliverables:
      - Reviewed content
      - Approval documentation
      - Change tracking
      - Sign-offs

  4_publication:
    activities:
      - CMS upload
      - Formatting check
      - Link validation
      - Schedule/publish

    deliverables:
      - Published content
      - Tracking setup
      - Promotion plan
      - Archive copy

  5_maintenance:
    activities:
      - Performance monitoring
      - Update scheduling
      - Feedback incorporation
      - Optimization

    triggers:
      - Age (>6 months)
      - Performance decline
      - Information changes
      - User feedback

content_retirement:
  criteria:
    - Outdated information
    - Poor performance
    - No longer relevant
    - Legal/compliance issues

  process:
    - Impact assessment
    - Redirect planning
    - Archive creation
    - Removal execution
```

#### Content Templates **[REQUIRED]**
```typescript
// templates/content-templates.ts
interface ContentTemplate {
  id: string;
  name: string;
  type: ContentType;
  structure: TemplateSection[];
  metadata: TemplateMetadata;
  variables: TemplateVariable[];
}

interface TemplateSection {
  name: string;
  type: 'heading' | 'paragraph' | 'list' | 'code' | 'media' | 'cta';
  required: boolean;
  guidelines: string;
  characterLimit?: number;
  example?: string;
}

interface TemplateVariable {
  key: string;
  type: 'text' | 'number' | 'date' | 'select' | 'boolean';
  required: boolean;
  default?: any;
  options?: string[];
  validation?: ValidationRule;
}

// Template library
const templates: Record<string, ContentTemplate> = {
  'blog-post': {
    id: 'blog-post',
    name: 'Blog Post Template',
    type: ContentType.Article,
    structure: [
      {
        name: 'headline',
        type: 'heading',
        required: true,
        guidelines: 'Compelling headline with primary keyword',
        characterLimit: 60,
        example: 'How to Improve Your Content Strategy in 2024'
      },
      {
        name: 'introduction',
        type: 'paragraph',
        required: true,
        guidelines: 'Hook reader and preview value',
        characterLimit: 150,
        example: 'Content strategy drives business growth...'
      },
      {
        name: 'mainContent',
        type: 'paragraph',
        required: true,
        guidelines: 'Detailed information with subheadings',
        example: 'Structured content with H2 and H3 tags...'
      },
      {
        name: 'conclusion',
        type: 'paragraph',
        required: true,
        guidelines: 'Summarize and include CTA',
        characterLimit: 200
      }
    ],
    metadata: {
      estimatedTime: '2-3 hours',
      skillLevel: 'intermediate',
      reviewRequired: true
    },
    variables: [
      {
        key: 'author',
        type: 'text',
        required: true
      },
      {
        key: 'category',
        type: 'select',
        required: true,
        options: ['Technology', 'Marketing', 'Design', 'Business']
      }
    ]
  }
};
```

### 8.2 Content Distribution

#### Multi-Channel Publishing **[REQUIRED]**
```yaml
# distribution-strategy.yaml
distribution_channels:
  owned_media:
    website:
      types: [blog, documentation, landing pages]
      frequency: "2-3 times per week"
      optimization: "SEO, CRO"

    email:
      types: [newsletter, drip campaigns, announcements]
      frequency: "Weekly newsletter, event-driven campaigns"
      optimization: "Subject lines, send times"

    mobile_app:
      types: [in-app messages, push notifications]
      frequency: "Based on user behavior"
      optimization: "Timing, personalization"

  earned_media:
    pr_outlets:
      types: [press releases, contributed articles]
      frequency: "Monthly or event-driven"
      requirements: "Newsworthy angle, media kit"

    influencers:
      types: [guest posts, interviews, reviews]
      frequency: "Quarterly campaigns"
      requirements: "Relationship building, value exchange"

  paid_media:
    search_ads:
      types: [Google Ads, Bing Ads]
      content: "Ad copy, landing pages"
      optimization: "Keywords, quality score"

    social_ads:
      types: [Facebook, LinkedIn, Twitter]
      content: "Visual ads, video, carousel"
      optimization: "Audience targeting, creative testing"

  shared_media:
    social_platforms:
      types: [organic posts, stories, live streams]
      frequency: "Daily to weekly per platform"
      optimization: "Timing, hashtags, engagement"

    communities:
      types: [forums, groups, Q&A sites]
      frequency: "Regular participation"
      optimization: "Value-first approach"

syndication_rules:
  content_adaptation:
    - Customize for each channel
    - Respect platform guidelines
    - Optimize format and length
    - Include platform-specific CTAs

  timing_strategy:
    - Publish on owned media first
    - Syndicate after 24-48 hours
    - Schedule for optimal engagement
    - Consider time zones

  tracking_requirements:
    - Use UTM parameters
    - Track referral sources
    - Monitor engagement metrics
    - Attribute conversions
```

#### Content Automation **[RECOMMENDED]**
```typescript
// automation/content-distributor.ts
interface DistributionPlan {
  contentId: string;
  channels: ChannelConfig[];
  schedule: DistributionSchedule;
  personalization?: PersonalizationRules;
  tracking: TrackingConfig;
}

interface ChannelConfig {
  channel: DistributionChannel;
  enabled: boolean;
  template?: string;
  customization?: ChannelCustomization;
  scheduling?: ChannelSchedule;
}

interface ChannelCustomization {
  title?: string;
  description?: string;
  image?: MediaAsset;
  cta?: string;
  hashtags?: string[];
  mentions?: string[];
}

class ContentDistributor {
  async distribute(plan: DistributionPlan): Promise<DistributionResult> {
    const results: ChannelResult[] = [];

    for (const channel of plan.channels) {
      if (!channel.enabled) continue;

      try {
        const adapted = await this.adaptContent(
          plan.contentId,
          channel
        );

        const result = await this.publishToChannel(
          adapted,
          channel
        );

        results.push({
          channel: channel.channel,
          success: true,
          url: result.url,
          metrics: result.metrics
        });
      } catch (error) {
        results.push({
          channel: channel.channel,
          success: false,
          error: error.message
        });
      }
    }

    return {
      contentId: plan.contentId,
      timestamp: new Date(),
      results: results,
      summary: this.generateSummary(results)
    };
  }

  private async adaptContent(
    contentId: string,
    channel: ChannelConfig
  ): Promise<AdaptedContent> {
    const content = await this.getContent(contentId);
    const adapter = this.getAdapter(channel.channel);

    return adapter.adapt(content, channel.customization);
  }
}

// Channel-specific adapters
class EmailAdapter implements ChannelAdapter {
  adapt(content: Content, customization?: ChannelCustomization): AdaptedContent {
    return {
      subject: customization?.title || this.generateSubject(content),
      preheader: this.generatePreheader(content),
      body: this.formatForEmail(content.body),
      cta: customization?.cta || content.defaultCta,
      unsubscribe: this.getUnsubscribeLink()
    };
  }
}
```

---

## Implementation Guidelines

### Content Strategy Rollout
1. **Assessment Phase**: Audit existing content and processes
2. **Planning Phase**: Develop content strategy and governance model
3. **Training Phase**: Educate teams on standards and tools
4. **Implementation Phase**: Roll out processes and templates
5. **Optimization Phase**: Monitor, measure, and refine

### Tool Requirements
- **CMS**: Headless or traditional with API access
- **Analytics**: Google Analytics, content-specific metrics
- **SEO Tools**: Keyword research, ranking tracking
- **Collaboration**: Editorial calendar, review workflows
- **Localization**: Translation management system

### Success Metrics
- **Quality Metrics**: Readability scores, error rates
- **Engagement Metrics**: Time on page, scroll depth
- **SEO Metrics**: Rankings, organic traffic
- **Conversion Metrics**: Goal completions, ROI
- **Efficiency Metrics**: Time to publish, review cycles

### Training Requirements
- **Writing Skills**: Style guide training, writing workshops
- **Technical Skills**: CMS training, SEO basics
- **Process Training**: Workflow understanding, tool usage
- **Quality Standards**: Review criteria, fact-checking
- **Continuous Learning**: Industry updates, best practices

---

**End of Content Standards**
