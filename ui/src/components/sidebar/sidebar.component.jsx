import { useState } from "react";
import { useEffect } from "react";
import "./sidebar.styles.css";
import { Link } from "react-router-dom";
import ApiUtils from "../../api/apiUtils";
import ApiEndpoints from "../../api/apiEndpoints";
import CommonUtil from "../../util/commonUtil";

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
  };

  useEffect(() => {
    fetchChatUser();
  }, []);

  const getConnectedUserIds = () => {
    let connectedUsers = "";
    for (let chatUser of chatUsers) {
      connectedUsers += chatUser.id + ",";
    }
    return connectedUsers.slice(0, -1);
  };

  const fetchUsers = async () => {
    const url = ApiEndpoints.USER_URL + "?exclude=" + getConnectedUserIds();
    const users = await ApiConnector.sendGetRequest(url);
    setUsers(users);
    console.log("фетч юзерс " + users)
  };

  const addPeopleClickHandler = async () => {
    await fetchUsers();
    setIsShowAddPeopleModal(true);
  };

  const getActiveChatClass = (roomId) => {
    let activeChatId = props.currentRoomId;
    console.log("айди чата " + activeChatId);
    //console.log("айди чата аргумент" + roomId);
    return roomId == activeChatId ? "-active-chat" : "";
  };

  const logoutClickHandler = () => {
    console.log("вышел")
  };

  const getChatListWithOnlineUser = () => {
    let updatedChatList = chatUsers.map((user) => {
    console.log("онлайн пользователи " + props.onlineUserList);
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
        <button onClick={addPeopleClickHandler}
          className="btn btn-outline-warning btn-block my-1 mt-4">
          Add People
        </button>
      
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
      <ModalWindow
        modalCloseHandler={() => setIsShowAddPeopleModal(false)}
        show={isShowAddPeopleModal}
      >
        {users.length > 0 ? (
          users?.map((user) => (
            <div
              key={user.id}
              className="d-flex align-items-start pt-1 pb-1 d-flex align-items-center"
            >
              <img
                src={user.image}
                className="rounded-circle mr-1"
                alt={user.username}
                width="40"
                height="40"
              />
              <div className="flex-grow-1 ml-2 mr-5">
                {user.username}
              </div>
              <button
                onClick={() => addMemberClickHandler(user.id)}
                className="btn btn-sm btn-success"
              >
                Add
              </button>
            </div>
          ))
        ) : (
          <h3>No More User Found</h3>
        )}
      </ModalWindow>
    </div>
  );
};

export default Sidebar;