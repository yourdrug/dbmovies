import { createContext, useState } from "react";

export const UserContext = createContext({
    currentUser: null,
    setCurrentUser: ()=> null,
    token: null,
    setToken: ()=> null,
});

export const UserProvider = ({children}) =>{
    const [currentUser, setCurrentUser] = useState(null)
    const [token, setToken] = useState(null)
    const value = {currentUser, setCurrentUser, token, setToken}
    return <UserContext.Provider value={value}>{ children }</UserContext.Provider>
}