package com.example.atlas;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import android.os.Bundle;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {

    private String name;
    private String uid;

    // Creation of the objects for TextView Welcome and ErrorLogin
    private TextView welcomeText;
    private TextView errorLogin;
    // Definition of the Login URL
    private String LOGIN_URL = "https://atlasserverapp.000webhostapp.com/loginuser";

    // Unable the back button so you can't return to app pressing it
    @Override
    public void onBackPressed() { }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // Get UI elements objects
        welcomeText = findViewById(R.id.welcome_text);
        errorLogin = findViewById(R.id.error_login);
        final EditText usernameText = findViewById(R.id.username_text);
        final EditText passwordText = findViewById(R.id.password_text);

        Button loginButton = findViewById(R.id.login_button);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Get username and password values when the button is pressed
                String username = usernameText.getText().toString();
                String password = passwordText.getText().toString();

                // Send a request to de url with the arguments
                requestLogin(LOGIN_URL, username, password);
            }
        });
    }

    private String getName(){
        return name;
    }

    private String getUid(){
        return uid;
    }

    private void requestLogin(String url, String username, String password) {
        RequestPackage requestPackage = new RequestPackage();
        // Set method and url
        requestPackage.setMethod("GET");
        requestPackage.setUrl(url);

        // Set username and password parameters
        requestPackage.setParam("username", username);
        requestPackage.setParam("password", password);

        loginThread LoginThread = new loginThread(); //Instantiation of the Async task
        //that’s defined below

        // We start the thread using the requestPackage created
        LoginThread.execute(requestPackage);
    }

    private class loginThread extends AsyncTask<RequestPackage, String, String> {
        @Override
        protected String doInBackground(RequestPackage... params) {
            return HttpManager.getData(params[0]);
        }

        //The String that is returned in the doInBackground() method is sent to the
        // onPostExecute() method below. The String should contain JSON data.
        @Override
        protected void onPostExecute(String result) {
            try {
                //We need to convert the string in result to a JSONArray
                JSONArray jsonArray = new JSONArray(result);

                //If the array length is not 0 then we have a correct login so we can
                //continue to de app.
                //If the array length is 0 then we have an incorrect login so we display
                //an incorrect login message.
                if(jsonArray.length() != 0){
                    JSONObject jsonObject = jsonArray.getJSONObject(0);
                    name = jsonObject.getString("name");
                    uid = jsonObject.getString("student_uid");

                    //We open the AppActivity, and we pass the name and uid variables so we
                    //can use them in the AppActivity
                    Intent i = new Intent(getApplicationContext(),AppActivity.class);
                    i.putExtra("name", getName());
                    i.putExtra("uid", getUid());
                    startActivity(i);
                } else {
                    //Make incorrect login message visible
                    errorLogin.setVisibility(View.VISIBLE);

                    //Make incorrect login invisible (gone) 2 seconds later
                    new android.os.Handler().postDelayed(
                            new Runnable() {
                                public void run() {
                                    errorLogin.setVisibility(View.GONE);
                                }
                            },
                            2000);
                }

            } catch (JSONException e) {
                e.printStackTrace();
           }
        }
    }
}