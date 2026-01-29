# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.

# Keep Parcelables
-keepnames class * implements android.os.Parcelable

# Keep Room entities
-keep @androidx.room.Entity class *
-dontwarn androidx.room.paging.**

# Keep data classes
-keep class com.kasir.data.** { *; }
-keep class com.kasir.model.** { *; }

# Apache POI
-dontwarn org.apache.poi.**
-dontwarn org.apache.xmlbeans.**
-dontwarn org.openxmlformats.schemas.**

# iText PDF
-dontwarn com.itextpdf.**
-keep class com.itextpdf.** { *; }
