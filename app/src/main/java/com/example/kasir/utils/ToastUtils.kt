package com.example.kasir.utils

import android.content.Context
import android.widget.Toast
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

object ToastUtils {
    fun showToast(context: Context, message: String, duration: Int = Toast.LENGTH_SHORT) {
        Toast.makeText(context, message, duration).show()
    }
    
    fun showLongToast(context: Context, message: String) {
        Toast.makeText(context, message, Toast.LENGTH_LONG).show()
    }
}

@Composable
fun rememberToast(): (String) -> Unit {
    val context = LocalContext.current
    return { message ->
        ToastUtils.showToast(context, message)
    }
}
