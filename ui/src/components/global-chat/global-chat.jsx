import { UserContext } from '../../context/user.context';
import { useContext, useState, useEffect } from 'react';
import SocketActions from "../../lib/socketActions";
import ServerUrl from "../../api/serverUrl";
import CommonUtil from "../../util/commonUtil";
import axios from 'axios';

import './global-chat.css'

const GlobalChat = ({active, setActive}) =>{
    const [onlineUserList, setOnlineUserList] = useState(null);
    const [onlineUsersCount, setOnlineUsersCount] = useState(0);
    const [inputMessage, setInputMessage] = useState("");
    const [messages, setMessages] = useState({});
    const { socket, currentUser, token } = useContext(UserContext);

    const fetchChatMessage = async () => {
      const currentRoomId = 3;
      const url = `http://127.0.0.1:8000/social/chats/${currentRoomId}/messages?limit=12&offset=0`
      let config = {
        headers: {
          Authorization: "Token " + token,
        },
    };
      const response =  await axios.get(url, config);
      const chatMessages = response.data;
      setMessages(chatMessages);
    };
  
    useEffect(() => {
      if(currentUser){
        fetchChatMessage();
      }
    }, [currentUser]);

    const messageSubmitHandler = (event) => {
      event.preventDefault();
      if (inputMessage) {
        socket.send(
          JSON.stringify({
            action: SocketActions.MESSAGE,
            message: inputMessage,
            user: currentUser.id,
            roomId: 3,
          })
        );
      }
      setInputMessage("");
    };
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log(data)
        if (data.action == SocketActions.MESSAGE) {
          data["userImage"] = ServerUrl.BASE_URL.slice(0, -1) + data.userImage;
          setMessages((prevState) => {
            let messagesState = JSON.parse(JSON.stringify(prevState));
            console.log("messagesState " + messagesState);
            messagesState.results.unshift(data);
            return messagesState;
          });
          console.log("coo,otybz " + messages);
        }
        if (data.action == SocketActions.ONLINE_USER) {
          setOnlineUserList(data.userList);
        }
        if (data.action == 'online_users_count') {
          setOnlineUsersCount(data.count);
        }
      };

    return(
      <div className='global-chat-container'>
        {active ? (
          <div className='modal-global-chat-content-active'>
            <div className='global-chat-user-counts'> 
              <div className="user-online-circle"/> &nbsp; {onlineUsersCount} 
              <div className='button-for-collapse' onClick={() => setActive(false)}> 
                <img 
                  src='https://cdn-icons-png.flaticon.com/512/54/54860.png'
                  width="30"
                  height="30"/> 
              </div>
            </div> 
            <div className="global-chat-messages-container">
              {messages?.results?.map((message, index) => (
                <div key={index} className="global-chat-message-left">
                  <div className="avatar-in-global-chat">
                    <img
                      src={message.userImage}
                      className="avatar-for-chatting-in-chat"
                      alt={message.username}
                      width="30"
                      height="30"
                    />
                  </div>
                  <div className="global-chat-message-body">
                    <div>
                      <span className='username-in-global-chat-message'>{message.username}</span>
                      <span className='text-in-global-chat-message'>{message.text}</span> 
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="global-chat-input-message-container">
              <form onSubmit={messageSubmitHandler}>
                <div className="input-group-for-global-chat">
                  <textarea
                    onChange={(event) => setInputMessage(event.target.value)}
                    value={inputMessage}
                    id="global-chat-message-input"
                    type="text"
                    className="form-control"
                    placeholder="Введите ваше сообщение"
                    autoComplete="off"
                  /> 
                </div>
              </form>
              <img
                src="https://cdn-icons-png.flaticon.com/128/736/736161.png"
                className="submit-btn-in-global-chat"
                alt="send"
                width="50"
                height="50"
                onClick={messageSubmitHandler}
              /> 
            </div>
          </div>
        ) : (
          <div className='modal-global-chat-content' onClick={() => setActive(true)}>
            <div className='global-chat-user-counts'> 
              <div className="user-online-circle"/> &nbsp; {onlineUsersCount} 
            </div>
          </div>
        )}
      </div>
    );
};

export default GlobalChat