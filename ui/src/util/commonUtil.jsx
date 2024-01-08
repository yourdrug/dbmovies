
const is_date = (date) => {
  if (Object.prototype.toString.call(date) === "[object Date]") {
    return true;
  }
  return false;
};

const getTimeFromDate = (date) => {
  let dateObj = is_date(date) ? date : new Date(date);
  let hour = dateObj.getHours();
  let minute = dateObj.getMinutes();
  let meridian = "am";
  if (hour > 12) {
    hour -= 12;
    meridian = "pm";
  }
  if (hour === 0) {
    hour = 12;
  }
  if (minute < 10) {
    minute = "0" + minute;
  }
  return hour + ":" + minute + " " + meridian;
};

const getFormatedChatUser = (chatUsers, onlineUserList) => {
  const userId = JSON.parse(localStorage.getItem("currentUser")).id
  return chatUsers.reduce((acumulator, item) => {
    if (item.type === "DM" || item.type === "SELF") {
      let newResult = {};
      newResult["roomId"] = item.id;
      let member = null;
      for (let user of item.users) {
        if (user.id != userId || item.type === "SELF") {
          member = user;
        }
      }
      if (member) {
        newResult["name"] = member.username;
        newResult["image"] = member.image;
        newResult["id"] = member.id;
        newResult["isOnline"] = onlineUserList?.includes(member.id);
      }
      acumulator.push(newResult);
      return acumulator;
    }
    return acumulator;
  }, []);
};

const CommonUtil = {
  getTimeFromDate: getTimeFromDate,
  getFormatedChatUser: getFormatedChatUser,
};

export default CommonUtil;
