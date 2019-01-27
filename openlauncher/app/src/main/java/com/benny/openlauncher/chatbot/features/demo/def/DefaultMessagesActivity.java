package com.benny.openlauncher.chatbot.features.demo.def;

import android.app.Fragment;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.content.res.Resources;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;

import android.widget.ImageView;
import com.benny.openlauncher.R;
import com.benny.openlauncher.chatbot.common.data.model.Message;
import com.benny.openlauncher.chatbot.common.data.model.User;
import com.benny.openlauncher.chatbot.utils.AppUtils;
import com.benny.openlauncher.model.App;
import com.stfalcon.chatkit.messages.MessageInput;
import com.stfalcon.chatkit.messages.MessagesList;
import com.stfalcon.chatkit.messages.MessagesListAdapter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.ArrayList;

public class DefaultMessagesActivity extends DemoMessagesActivity
    implements MessageInput.InputListener,
    MessageInput.TypingListener {

  User conscience;
  String token = "iyoetqma1nybfiw3g2qmuy0px3ws9qwdls43ljn7xc54lmr6w9ul2p33u26mdo98olhwpwl2vhl2589io8tt86l7t8m8sy21pkn3wocy78cpnmjsqzw1uy2ds86tzef3";

  public static void open(Context context) {
    context.startActivity(new Intent(context, DefaultMessagesActivity.class));
  }

  private MessagesList messagesList;
  private String app_package_name;
  private String app_name;


  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_default_messages);

    super.messages = new ArrayList<>();

    this.messagesList = (MessagesList) findViewById(R.id.messagesList);
    initAdapter();

    MessageInput input = (MessageInput) findViewById(R.id.input);
    input.setInputListener(this);
    input.setTypingListener(this);

    Bundle bundle = getIntent().getExtras();
    String app_package_name = bundle.getString("app_package_name");
    this.app_package_name = app_package_name;
    this.app_name = bundle.getString("app_name");
    try
    {
      ImageView app_icon_view = findViewById(R.id.app_icon_view);
      Drawable icon = getPackageManager().getApplicationIcon(app_package_name);
      app_icon_view.setImageDrawable(icon);
    }
    catch (PackageManager.NameNotFoundException e) {
      e.printStackTrace();
    }

    conscience = new User("1", "Your conscience", "https://cdn4.iconfinder.com/data/icons/smashicons-movies-flat/58/17_-_Yoda_Flat-512.png", true);
    super.messagesAdapter.addToStart(new Message("Why?", conscience, "Why?"), true);
  }

  @Override
  public boolean onSubmit(CharSequence input) {
    Message newMessage = new Message(input.toString(), new User("0", "hi", "", true), input.toString());
    super.messagesAdapter.addToStart(newMessage, true);
    Message response = new Message("Okay, thanks!", conscience, "Okay, thanks!");
    super.messagesAdapter.addToStart(response, true);
    Handler handler = new Handler();

//    postRequest();
    handler.postDelayed(new Runnable() {
      @Override
      public void run() {
        Intent originalApp = getPackageManager().getLaunchIntentForPackage(app_package_name);
        originalApp.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(originalApp);
        finish();
      }
    }, 1000);
    return true;
  }

  public void postRequest(){
    try {
      String spacelessname = app_name.replace(" ", "%20");
      URL url = new URL("http:/10.0.2.2/api/app/"+app_package_name+"/create?token="+token+"&name="+spacelessname+"&icon=");

      HttpURLConnection conn = (HttpURLConnection) url.openConnection();
      conn.setRequestMethod("POST");
//        conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
      conn.setRequestProperty("Accept","application/json");
      conn.setDoOutput(true);
      conn.setDoInput(false);
      conn.connect();
//        Log.i("JSON", jsonParam.toString());
      DataOutputStream os = new DataOutputStream(conn.getOutputStream());
      //os.writeBytes(URLEncoder.encode(jsonParam.toString(), "UTF-8"));

//        os.flush();
//        os.close();

      Log.i("STATUS", String.valueOf(conn.getResponseCode()));
      Log.i("MSG" , conn.getResponseMessage());

      conn.disconnect();
      // Simulate network access.
    } catch (
        ProtocolException e) {
      e.printStackTrace();
    } catch (
        MalformedURLException e) {
      e.printStackTrace();
    } catch (
        IOException e) {
      e.printStackTrace();
    }
  }


  private void initAdapter() {
    super.messagesAdapter = new MessagesListAdapter<>(super.senderId, super.imageLoader);
    super.messagesAdapter.enableSelectionMode(this);
    super.messagesAdapter.setLoadMoreListener(this);
    super.messagesAdapter.registerViewClickListener(R.id.messageUserAvatar,
        (view, message) -> AppUtils.showToast(DefaultMessagesActivity.this,
            "Listen to your conscience",
            false));
    this.messagesList.setAdapter(super.messagesAdapter);
  }

  @Override
  public void onStartTyping() {
    Log.v("Typing listener", getString(R.string.start_typing_status));
  }

  @Override
  public void onStopTyping() {
    Log.v("Typing listener", getString(R.string.stop_typing_status));
  }
}
