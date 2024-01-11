import { createContext, useState } from "react";

export const UserContext = createContext({
    currentUser: null,
    setCurrentUser: ()=> null,
    token: null,
    setToken: ()=> null,
    socket: null,
    setSocket: ()=> null,
});

export const UserProvider = ({children}) =>{
    const [currentUser, setCurrentUser] = useState(JSON.parse(localStorage.getItem("currentUser")))
    const [token, setToken] = useState(localStorage.getItem("token"))
    const [socket, setSocket] = useState({})
    const value = {currentUser, setCurrentUser, token, setToken, socket, setSocket}
    return <UserContext.Provider value={value}>{ children }</UserContext.Provider>
}