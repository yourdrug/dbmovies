import React, { useEffect, useState } from "react";
import ApiUtils from "../../api/apiUtils";
import ServerUrl from "../../api/serverUrl";
import SocketActions from "../../lib/socketActions";
import CommonUtil from "../../util/commonUtil";
import "./chat-body.css";

import axios from "axios";
import { Link } from "react-router-dom";

let socket

let typingTimer = 0;
let isTypingSignalSent = false;

const ChatBody = ({currentUser, currentRoomId, currentChattingMember, setOnlineUserList }) => {
  const [inputMessage, setInputMessage] = useState("");
  const [messages, setMessages] = useState({});
  const [typing, setTyping] = useState(false);

  if (currentUser){
    socket = new WebSocket(
      ServerUrl.WS_BASE_URL + `ws/users/${JSON.parse(localStorage.getItem("currentUser")).id}/chat/`
    );
  }

  const fetchChatMessage = async () => {
    const currentChatId = currentRoomId;
    if (currentChatId) {
      const url = `http://127.0.0.1:8000/social/chats/${currentChatId}/messages?limit=12&offset=0`
      const config = { headers: ApiUtils.getAuthHeader() };
      const response =  await axios.get(url, config);
      const chatMessages = response.data;
      setMessages(chatMessages);
    }
  };

  useEffect(() => {
    fetchChatMessage();
  }, [currentRoomId]);

  const loggedInUserId = currentUser.id;
  const getChatMessageClassName = (userId) => {
    return loggedInUserId == userId
      ? "chat-message-right"
      : "chat-message-left";
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const chatId = currentRoomId;
    const userId = currentUser.id;
    if (chatId === data.roomId) {
      if (data.action === SocketActions.MESSAGE) {
        data["userImage"] = ServerUrl.BASE_URL.slice(0, -1) + data.userImage;
        setMessages((prevState) => {
          let messagesState = JSON.parse(JSON.stringify(prevState));
          messagesState.results.unshift(data);
          return messagesState;
        });
        setTyping(false);
      } else if (data.action === SocketActions.TYPING && data.user !== userId) {
        setTyping(data.typing);
      }
    }
    if (data.action === SocketActions.ONLINE_USER) {
      setOnlineUserList(data.userList);
    }
  };

  const messageSubmitHandler = (event) => {
    event.preventDefault();
    if (inputMessage) {
      socket.send(
        JSON.stringify({
          action: SocketActions.MESSAGE,
          message: inputMessage,
          user: currentUser.id,
          roomId: currentRoomId,
        })
      );
    }
    setInputMessage("");
  };

  const sendTypingSignal = (typing) => {
    socket.send(
      JSON.stringify({
        action: SocketActions.TYPING,
        typing: typing,
        user: currentUser.id,
        roomId: currentRoomId,
      })
    );
  };

  const chatMessageTypingHandler = (event) => {
    if (event.keyCode !== Constants.ENTER_KEY_CODE) {
      if (!isTypingSignalSent) {
        sendTypingSignal(true);
        isTypingSignalSent = true;
      }
      clearTimeout(typingTimer);
      typingTimer = setTimeout(() => {
        sendTypingSignal(false);
        isTypingSignalSent = false;
      }, 3000);
    } else {
      clearTimeout(typingTimer);
      isTypingSignalSent = false;
      messageSubmitHandler(event);
    }
  };

  return (
    <>
    {currentRoomId ? (
      <div className="chat-container">
      <div className="header">
        <div className="user-info">
          {currentChattingMember?.isOnline ? (
            <div className="circle-and-info-about-online">
              <div className="user-online-circle">&nbsp;</div>
            </div> ) : (
            <div className="circle-and-info-about-online"> 
              <div className="user-offline-circle">&nbsp;</div>
            </div> )}
          <img
            src={currentChattingMember?.image}
            className="user-image-container"
            alt="User"
            width="40"
            height="40"
          />
          <div className="user-name">
            <strong>{currentChattingMember?.name}</strong>
          </div>
        </div>
      </div>
      <div className="chat-messages-container">
           {typing && (
            <div className="chat-message-left chat-bubble mb-1">
              <div className="typing">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          )}
          {messages?.results?.map((message, index) => (
            <div key={index} className={getChatMessageClassName(message.sender)}>
              <div className="avatar-in-chat">
                <img
                  src={message.userImage}
                  className="avatar-for-chatting-in-chat"
                  alt={message.username}
                  width="40"
                  height="40"
                />
              </div>
              <div className="chat-message-body">
                <div className="username-time-for-messages-in-chat">
                  <div> {message.username}&nbsp; </div> 
                  <div> {CommonUtil.getTimeFromDate(message.created)} </div>
                </div>
                <div className="text-in-chat-message">
                  {message.text}
                </div>
              </div>
              
            </div>
          ))}
      </div>
      <div className="chatting-input-message">
        <form onSubmit={messageSubmitHandler}>
          <div className="input-group">
            <textarea
              onChange={(event) => setInputMessage(event.target.value)}
              onKeyUp={chatMessageTypingHandler}
              value={inputMessage}
              id="chat-message-input"
              type="text"
              className="form-control"
              placeholder="Введите ваше сообщение"
              autoComplete="off"
            />
            <button className="btn-for-sending-messages"> Отправить </button>
          </div>
        </form>
      </div>
    </div>
    ) : (
      <div className="no-chat-selected-div">
        <div className="message-for-choose-chat"> Выберите чат, чтобы начать переписываться </div>
      </div>
    )}
  </>
  );
};

export default ChatBody;