import { useState, useContext } from "react";
import ChatBody from "../../components/chat-body/chat-body.component";
import Sidebar from "../../components/sidebar/sidebar.component";

import './chatting.styles.css'
import { UserContext } from "../../context/user.context";

const HomeScreen = () => {
  const [currentChattingMember, setCurrentChattingMember] = useState({});
  const [onlineUserList, setOnlineUserList] = useState([]);
  const [currentRoomId, setCurrentRoomId] = useState();

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