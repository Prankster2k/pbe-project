package com.example.atlas;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Iterator;


public class AppActivity extends AppCompatActivity {

    private String URL = "https://atlasserverapp.000webhostapp.com";

    private TextView welcomeText;
    private TableLayout dataTable;
    private String name;
    private String uid;

    // Unable the back button so you can't return to login pressing it
    @Override
    public void onBackPressed() { }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_app);

        //Set name and uid variables
        name = getIntent().getStringExtra("name");
        uid = getIntent().getStringExtra("uid");

        //Set Welcome text with the name of the user
        welcomeText = findViewById(R.id.welcome_text);
        welcomeText.setText("Welcome " + name);

        //Define de searchBar object and the dataTable object
        final EditText searchBar = findViewById(R.id.search_bar);
        dataTable = findViewById(R.id.data_table);

        Button searchButton = findViewById(R.id.search_button);
        searchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                // Get the query form the search bar when the button is pressed
                String query = searchBar.getText().toString();

                // Send a request to de url with the arguments
                requestSearch(URL, query, uid);
            }
        });

        Button logoutButton = findViewById(R.id.logout_button);
        logoutButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                Intent i = new Intent(getApplicationContext(),LoginActivity.class);
                startActivity(i);
            }
        });

        searchBar.setOnKeyListener(new View.OnKeyListener() {
            @Override
            public boolean onKey(View view, int keyCode, KeyEvent keyEvent) {
                if ((keyEvent.getAction() == KeyEvent.ACTION_DOWN) &&
                        (keyCode == KeyEvent.KEYCODE_ENTER)) {
                    // Perform action on key press

                    // Get the query form the search bar when the button is pressed
                    String query = searchBar.getText().toString();

                    // Send a request to de url with the arguments
                    requestSearch(URL, query, uid);
                }
                return false;
            }
        });

    }

    private void requestSearch(String url, String query, String uid) {
        RequestPackage requestPackage = new RequestPackage();
        // Set method and url
        requestPackage.setMethod("GET");
        //Get URL path and add it to the url
        String[] queryParts = query.split("\\?");
        requestPackage.setUrl(url + "/" + queryParts[0]);

        //Set parameter in the query using queryParts
        if(queryParts.length > 1) {
            String[] parmsAndValues = queryParts[1].split("&");
            for (int i = 0; i < parmsAndValues.length; i++) {
                String[] parmValue = parmsAndValues[i].split("=");
                requestPackage.setParam(parmValue[0], parmValue[1]);
            }
        }
        // Set the uid parameter
        requestPackage.setParam("uid", uid);

        AppActivity.searchThread SearchThread = new AppActivity.searchThread(); //Instantiation of the Async task
        //that’s defined below

        // We start the thread using the requestPackage created
        SearchThread.execute(requestPackage);
    }

    private class searchThread extends AsyncTask<RequestPackage, String, String> {
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

                generateTable(jsonArray);

            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    protected void generateTable(JSONArray jsonArray){
        try{
            //We clean the table
            dataTable.removeAllViews();

            //We will save all our TextViews in an array called table
            int i = 0;
            ArrayList<TextView> tableObjects = new ArrayList<>();

            //First we get the header
            TableRow header = new TableRow(this);
            header.setGravity(Gravity.CENTER);

            Iterator<String> it = jsonArray.getJSONObject(0).keys();
            while(it.hasNext()){
                String key = it.next();

                TextView tableObj = new TextView(this);
                tableObj.setText(key.toUpperCase());
                tableObj.setTextColor(Color.BLACK);
                tableObj.setTypeface(null, Typeface.BOLD);
                tableObj.setTextSize(12);
                tableObj.setPadding(10, 10, 10, 10);
                tableObj.setGravity(Gravity.CENTER);
                tableObjects.add(tableObj);

                header.addView(tableObjects.get(i));

                i++;
            }
            dataTable.addView(header);

            //Put the data
            ArrayList<TableRow> infoRows = new ArrayList<>();
            TableRow infoRow = new TableRow(this);;

            for(int j = 0; j < jsonArray.length(); j++){
                infoRow = new TableRow(this);

                it = jsonArray.getJSONObject(0).keys();
                while(it.hasNext()){
                    String key = it.next();

                    TextView tableObj = new TextView(this);
                    tableObj.setText(jsonArray.getJSONObject(j).getString(key));
                    tableObj.setTextColor(Color.BLACK);
                    tableObj.setTextSize(8);
                    tableObj.setPadding(20, 20, 20, 20);
                    tableObj.setGravity(Gravity.CENTER);
                    tableObjects.add(tableObj);

                    infoRow.addView(tableObjects.get(i));

                    i++;
                }
                infoRow.setGravity(Gravity.CENTER);
                infoRows.add(infoRow);
                if(j % 2 != 0){
                    infoRow.setBackgroundColor(Color.rgb(220, 220, 220));
                }
                dataTable.addView(infoRows.get(j));
            }



        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}