import { useState, useContext } from "react";
import { useParams } from "react-router-dom";

import ChatBody from "../../components/chat-body/chat-body";
import Sidebar from "../../components/sidebar/sidebar";

import './chatting.css'
import { UserContext } from "../../context/user.context";

const HomeScreen = () => {
  const params = useParams();
  let chatId = params.chatId;

  const [currentChattingMember, setCurrentChattingMember] = useState({});
  const [onlineUserList, setOnlineUserList] = useState([]);
  const [currentRoomId, setCurrentRoomId] = useState(chatId);

  const { currentUser, token } = useContext(UserContext) 

  return (
    <div className="main-wrapper">
      <div className="chat-screen-container">
          <Sidebar
            currentUser={currentUser}
            currentRoomId={currentRoomId}
            setCurrentRoomId={setCurrentRoomId}
            setCurrentChattingMember={setCurrentChattingMember}
            onlineUserList={onlineUserList}
          />
          <ChatBody
            currentUser={currentUser}
            currentRoomId={currentRoomId}
            setCurrentRoomId={setCurrentRoomId}
            setOnlineUserList={setOnlineUserList}
            currentChattingMember={currentChattingMember}
          />
        </div>
    </div>
  );
};

export default HomeScreen;