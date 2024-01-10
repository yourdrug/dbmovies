import { useState } from "react";
import { useEffect } from "react";
import "./sidebar.css";
import { Link } from "react-router-dom";
import ApiUtils from "../../api/apiUtils";
import ApiEndpoints from "../../api/apiEndpoints";
import CommonUtil from "../../util/commonUtil";
import Modal from "../modal/modal";

import axios from "axios";

const Sidebar = (props) => {
  const [chatUsers, setChatUsers] = useState([]); //sidebar users
  const [users, setUsers] = useState([]); //popup users
  const [isShowAddPeopleModal, setIsShowAddPeopleModal] = useState(false);

  const fetchChatUser = async () => {
    const userId = props.currentUser.id;   
    const url = `http://127.0.0.1:8000/social/users/${userId}/chats`;
    const config = { headers: ApiUtils.getAuthHeader() };
    const response =  await axios.get(url, config);
    const chatUsers = response.data;
    const formatedChatUser = CommonUtil.getFormatedChatUser(
      chatUsers,
      props.onlineUserList
    );
    setChatUsers(formatedChatUser);
    let currentChattingMember = formatedChatUser.find(room => room.roomId == props.currentRoomId) || null;
    props.setCurrentChattingMember(currentChattingMember);
  };

  const getConnectedUserIds = () => {
    let connectedUsers = "";
    for (let chatUser of chatUsers) {
      connectedUsers += chatUser.id + ",";
    }
    return connectedUsers.slice(0, -1);
  };

  useEffect(() => {
    fetchChatUser();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/users/?exclude=' + getConnectedUserIds());
      let info = await response.data.results;
      setUsers(info);
    } catch (error) {
      alert("ошибка в получении данных с сервера");
    }
  };

  const addPeopleClickHandler = async () => {
    await fetchUsers();
    setIsShowAddPeopleModal(true);
  };

  const handleUserNewChatClick = async (user) => {
    try {
      let data = {}
      if(props.currentUser.id == user.id){
        data = {
          'members': [user.id],
          'type': "SELF",
          'name': user.username
        };
      }

      else{
        data = {
          'members': [props.currentUser.id, user.id],
          'type': "DM",
          'name': user.username
        };
      }
      
      const response = await axios.post('http://127.0.0.1:8000/social/chats', data);
      console.log(response.data);
    } catch (error) {
      console.log(error);
      alert(error.message);
    }
  };

  const getActiveChatClass = (roomId) => {
    let activeChatId = props.currentRoomId;
    return roomId == activeChatId ? "-active-chat" : "";
  };

  const getChatListWithOnlineUser = () => {
    let updatedChatList = chatUsers.map((user) => {
      if (props.onlineUserList.includes(user.id)) {
        user.isOnline = true;
      } else {
        user.isOnline = false;
      }
      return user;
    });
    return updatedChatList;
  };

  return (
    <div className="all-users-chats-container">
        <button className='add-chats-for-sidebar' onClick={addPeopleClickHandler}>
          Добавить чат
        </button>
        <Modal active={isShowAddPeopleModal} setActive={setIsShowAddPeopleModal}>
          {users.map((user) => (
            <div className="additional-info-for-user" key={user.id} onClick={()=> handleUserNewChatClick(user)}>
              <img
                  src={user.image}
                  className="chat-user-avatar"
                  alt={user.name}
                  width="50"
                  height="50"
                />
              <div className="user-username-isonline">
                  {user.username}
                  {props.onlineUserList.includes(user.id) ? (
                    <div className="circle-and-info-about-online">
                      <div className="user-online-circle">&nbsp;</div>
                      &nbsp;  Online
                    </div> 
                    ) : (
                      <div className="circle-and-info-about-online"> 
                        <div className="user-offline-circle"></div>
                        &nbsp;  Offline
                      </div>
                    )}
                </div>
            </div>
          ))}
        </Modal>
      
      <div className="user-list-container" >
        {getChatListWithOnlineUser()?.map((chatUser, index) => {
          return (
            <Link
              onClick={() => {props.setCurrentChattingMember(chatUser); props.setCurrentRoomId(chatUser.roomId)}}
              to={`/chatting/${chatUser.roomId}`}
              className={"current-user-item-link"}
              key={index}
              style={{ textDecoration: 'none' }}
              >
              <div className={"additional-info-for-user" + getActiveChatClass(chatUser.roomId)}>
                <img
                  src={chatUser.image}
                  className="chat-user-avatar"
                  alt={chatUser.name}
                  width="50"
                  height="50"
                />
                <div className="user-username-isonline">
                  {chatUser.name}
                  {chatUser.isOnline ? (
                    <div className="circle-and-info-about-online">
                      <div className="user-online-circle">&nbsp;</div>
                      &nbsp;  Online
                    </div> 
                    ) : (
                      <div className="circle-and-info-about-online"> 
                        <div className="user-offline-circle"></div>
                        &nbsp;  Offline
                      </div>
                    )}
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default Sidebar;