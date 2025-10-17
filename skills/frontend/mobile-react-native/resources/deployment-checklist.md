# React Native Deployment Checklist

## Pre-Deployment

### Code Quality

- [ ] All tests passing (unit, integration, E2E)
- [ ] No console.log statements in production code
- [ ] Remove development/debug code
- [ ] Code reviewed and approved
- [ ] No hardcoded API URLs or secrets
- [ ] Environment variables properly configured

### Performance

- [ ] Images optimized (proper sizes, formats)
- [ ] Bundle size analyzed and optimized
- [ ] Performance profiling completed
- [ ] Memory leaks checked and fixed
- [ ] Network requests optimized (caching, batching)
- [ ] FlatList/SectionList used for long lists

### Security

- [ ] API keys stored securely (not in code)
- [ ] SSL/TLS certificate pinning implemented
- [ ] User input validation on all forms
- [ ] Authentication tokens stored securely
- [ ] Sensitive data encrypted
- [ ] Deep linking validated and secured

### Accessibility

- [ ] All interactive elements have accessibility labels
- [ ] Screen reader tested on iOS (VoiceOver)
- [ ] Screen reader tested on Android (TalkBack)
- [ ] Color contrast meets WCAG standards
- [ ] Touch targets at least 44x44 points

## iOS App Store Deployment

### Preparation

- [ ] Apple Developer account active
- [ ] App ID created in App Store Connect
- [ ] Provisioning profiles configured
- [ ] Distribution certificate valid
- [ ] App icons provided (all sizes)
- [ ] Launch screens created
- [ ] Privacy policy URL ready

### Build Configuration

```bash
# Update version and build number
# ios/YourApp/Info.plist
<key>CFBundleShortVersionString</key>
<string>1.0.0</string>
<key>CFBundleVersion</key>
<string>1</string>
```

### Build Steps

```bash
# 1. Install pods
cd ios && pod install && cd ..

# 2. Open Xcode
open ios/YourApp.xcworkspace

# 3. In Xcode:
# - Select "Any iOS Device (arm64)" as target
# - Product > Archive
# - Window > Organizer
# - Select archive > Distribute App
# - App Store Connect > Upload
```

### App Store Connect

- [ ] App metadata filled (name, description, keywords)
- [ ] Screenshots uploaded (all required sizes)
- [ ] App preview videos added (optional)
- [ ] Age rating completed
- [ ] App Review Information provided
- [ ] Test user account credentials (if required)
- [ ] Build selected and submitted for review

### Post-Submission

- [ ] Monitor App Review status
- [ ] Respond to review feedback promptly
- [ ] Test on TestFlight before public release
- [ ] Prepare release notes

## Android Play Store Deployment

### Preparation

- [ ] Google Play Developer account active
- [ ] App created in Play Console
- [ ] Signing key generated and backed up
- [ ] App icons provided (all densities)
- [ ] Feature graphic created (1024x500)
- [ ] Privacy policy URL ready

### Signing Configuration

```bash
# Generate signing key (first time only)
keytool -genkeypair -v -storetype PKCS12 \
  -keystore my-release-key.keystore \
  -alias my-key-alias \
  -keyalg RSA -keysize 2048 \
  -validity 10000
```

```gradle
// android/app/build.gradle
android {
  signingConfigs {
    release {
      storeFile file('my-release-key.keystore')
      storePassword 'YOUR_STORE_PASSWORD'
      keyAlias 'my-key-alias'
      keyPassword 'YOUR_KEY_PASSWORD'
    }
  }
  buildTypes {
    release {
      signingConfig signingConfigs.release
      minifyEnabled true
      proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
    }
  }
}
```

### Build Steps

```bash
# 1. Clean build
cd android && ./gradlew clean && cd ..

# 2. Build release bundle (AAB preferred)
cd android && ./gradlew bundleRelease

# 3. Or build APK
cd android && ./gradlew assembleRelease

# Output locations:
# AAB: android/app/build/outputs/bundle/release/app-release.aab
# APK: android/app/build/outputs/apk/release/app-release.apk
```

### Play Console Configuration

- [ ] Store listing completed
  - [ ] App name and short description
  - [ ] Full description (up to 4000 characters)
  - [ ] Screenshots (phone, tablet, 7-inch, 10-inch)
  - [ ] Feature graphic
  - [ ] App icon (512x512)
- [ ] Content rating completed
- [ ] Pricing and distribution set
- [ ] App access explained (if login required)
- [ ] Data safety form completed
- [ ] Release details:
  - [ ] Release name/version
  - [ ] Release notes (per language)
  - [ ] AAB/APK uploaded
  - [ ] Release to production/beta/alpha

### Post-Submission

- [ ] Monitor review status
- [ ] Test on internal/beta track first
- [ ] Roll out gradually (staged rollout)
- [ ] Monitor crash reports and ANRs

## Over-the-Air (OTA) Updates

### CodePush Setup

```bash
# Install CodePush CLI
npm install -g appcenter-cli

# Login
appcenter login

# Register app
appcenter apps create -d MyApp-iOS -o iOS -p React-Native
appcenter apps create -d MyApp-Android -o Android -p React-Native
```

### Deploy Update

```bash
# Release to production
appcenter codepush release-react -a <ownerName>/MyApp-iOS -d Production
appcenter codepush release-react -a <ownerName>/MyApp-Android -d Production

# Release to staging
appcenter codepush release-react -a <ownerName>/MyApp-iOS -d Staging
```

### OTA Best Practices

- [ ] Only use for JS/asset changes (not native code)
- [ ] Test updates on staging first
- [ ] Roll out gradually (10%, 25%, 50%, 100%)
- [ ] Monitor crash rates after deployment
- [ ] Keep rollback option ready
- [ ] Inform users of updates if significant

## Post-Deployment Monitoring

### Analytics

- [ ] Crash reporting configured (Sentry, Firebase)
- [ ] Analytics tracking implemented
- [ ] Performance monitoring active
- [ ] User engagement metrics tracked

### Monitoring Checklist

- [ ] Monitor crash-free rate (target: >99%)
- [ ] Track app launch time
- [ ] Monitor API response times
- [ ] Watch user retention rates
- [ ] Check review ratings and feedback
- [ ] Monitor network error rates

### Maintenance

- [ ] Regular dependency updates
- [ ] Security patches applied promptly
- [ ] Performance optimization ongoing
- [ ] User feedback reviewed and addressed
- [ ] Bug fixes prioritized and deployed

## Version Numbering

### Semantic Versioning

- **Major** (1.x.x): Breaking changes
- **Minor** (x.1.x): New features, backward compatible
- **Patch** (x.x.1): Bug fixes

### Build Numbers

- iOS: Increment for every build
- Android: versionCode in build.gradle (integer)

### Example

- Version: 1.2.3
- iOS Build: 15
- Android versionCode: 123015

## Emergency Rollback Plan

### iOS

- [ ] Previous version archived and available
- [ ] Emergency update prepared
- [ ] Expedited review requested if needed

### Android

- [ ] Previous APK/AAB backed up
- [ ] Can halt rollout immediately
- [ ] Emergency update prepared

### OTA (CodePush)

```bash
# Rollback to previous release
appcenter codepush rollback <ownerName>/<appName> Production

# Promote release from staging
appcenter codepush promote <ownerName>/<appName> Staging Production
```

## Compliance and Legal

- [ ] Privacy policy available and linked
- [ ] Terms of service available
- [ ] GDPR compliance (if applicable)
- [ ] COPPA compliance (if targeting children)
- [ ] Data collection disclosure complete
- [ ] Third-party SDK compliance verified
- [ ] Export compliance completed (iOS)

## Resources

- [iOS App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Android Play Store Policies](https://play.google.com/about/developer-content-policy/)
- [React Native Release Process](https://reactnative.dev/docs/signed-apk-android)
- [CodePush Documentation](https://docs.microsoft.com/en-us/appcenter/distribution/codepush/)
