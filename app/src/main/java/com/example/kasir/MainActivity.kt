package com.example.kasir

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import com.example.kasir.ui.navigation.KasirNavigation
import com.example.kasir.ui.theme.KasirTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        // Install splash screen before super.onCreate()
        val splashScreen = installSplashScreen()
        
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        // Keep splash screen visible while loading
        splashScreen.setKeepOnScreenCondition { false }
        
        setContent {
            KasirTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    KasirNavigation(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}
