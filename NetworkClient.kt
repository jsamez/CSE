
package com.example.text;

import android.util.Log;
import kotlinx.coroutines.Dispatchers;
import kotlinx.coroutines.withContext;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

class NetworkClient(private val serverIp: String, private val serverPort: Int) {
    private var socket: Socket? = null;
    private var bufferedReader: BufferedReader? = null;

    suspend fun connectToServer(): Boolean {
        return withContext(Dispatchers.IO) {
            try {
                socket = Socket(serverIp, serverPort);
                bufferedReader = BufferedReader(InputStreamReader(socket!!.getInputStream()));
                notifyServerConnectionSuccess();
                true;
            } catch (e: IOException) {
                notifyServerConnectionFailure();
                Log.e("NetworkClient", "Error during communication", e);
                false;
            }
        }
    }

    suspend fun receiveMessageWithTimestamp(): String {
        return withContext(Dispatchers.IO) {
            try {
                var clientSocketIn = socket!!.getInputStream();
                var tmp = clientSocketIn!!.bufferedReader(Charsets.UTF_8);
                if(tmp.ready()){
                    val message = bufferedReader?.readLine();
                    message.orEmpty();
                } else {
                    " ";
                }
            } catch (e: IOException) {
                Log.e("NetworkClient", "Error during communication", e);
                "Error: ${e.message}";
            }
        }
    }

    fun closeConnection() {
        bufferedReader?.close();
        socket?.close();
    }

    private fun notifyServerConnectionSuccess() {
        // 연결 성공 시 처리
    }

    private fun notifyServerConnectionFailure() {
        // 연결 실패 시 처리
    }
}
