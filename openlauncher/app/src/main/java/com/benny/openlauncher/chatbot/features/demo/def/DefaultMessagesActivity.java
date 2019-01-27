package com.benny.openlauncher.chatbot.features.demo.def;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.content.res.Resources;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
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
import java.util.ArrayList;

public class DefaultMessagesActivity extends DemoMessagesActivity
    implements MessageInput.InputListener,
    MessageInput.TypingListener {

  public static void open(Context context) {
    context.startActivity(new Intent(context, DefaultMessagesActivity.class));
  }

  private MessagesList messagesList;
  private String app_package_name;


  @Override
  protected void onCreate(Bundle savedInstanceState) {
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
    try
    {
      ImageView app_icon_view = findViewById(R.id.app_icon_view);
      Drawable icon = getPackageManager().getApplicationIcon(app_package_name);
      app_icon_view.setImageDrawable(icon);
    }
    catch (PackageManager.NameNotFoundException e) {
      e.printStackTrace();
    }

    User conscience = new User("1", "Your conscience", "https://cdn4.iconfinder.com/data/icons/smashicons-movies-flat/58/17_-_Yoda_Flat-512.png", true);
    super.messagesAdapter.addToStart(new Message("Why?", conscience, "Why?"), true);
  }

  @Override
  public boolean onSubmit(CharSequence input) {
    Message newMessage = new Message(input.toString(), new User("0", "hi", "", true), input.toString());
    super.messagesAdapter.addToStart(newMessage, true);
    Intent originalApp = getPackageManager().getLaunchIntentForPackage(app_package_name);
    originalApp.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
    startActivity(originalApp);
    finish();
    return true;
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
