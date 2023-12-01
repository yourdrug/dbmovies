import { useState, useContext, useEffect } from 'react'
import axios from 'axios'
import './login-form.styles.css'
import { UserContext } from '../../context/user.context'

const LoginForm = () =>{
    const [password, setPassword] = useState("")
    const [username, setUsername] = useState("")

    const { currentUser, setCurrentUser, setToken, token } = useContext(UserContext) 

    async function getAccountInfo() {
        let config = {
          headers: {
            Authorization: "Token " + token,
          },
        };
        try {
          const response = await axios.get(
            "http://127.0.0.1:8000/auth/users/me/",
            config
          );
          setCurrentUser(response.data);
        } catch (error) {
          alert(error.message);
        }
    }

    async function login() {
        let data = { username: username, password: password};
        try {
          const response = await axios.post(
            "http://127.0.0.1:8000/auth/token/login/",
            data
          );
          setToken(response.data.auth_token);
        } catch (error) {
          alert(error.message);
        }
    }

    async function logout() {
        let data = { username: username, password: password};
        let config = {
            headers: {
              Authorization: "Token " + token,
            },
          };
        axios.post("http://127.0.0.1:8000/auth/token/logout/", data, config)
            .then(() => {
                setCurrentUser(null);
                setToken(null);
            })
            .catch(error => {
                alert(error.message);
            });
    }

    useEffect(() => {
        if (token !== null) {
            getAccountInfo();
        }
    }, [token]);

    return(
        <div className='login-from'>
            <h1 className='title'>Войдите или зарегистрируйтесь</h1>
            <input className='username' value={username} 
            onChange={(event) => setUsername(event.target.value)} 
            type='text' placeholder='Имя пользователя'/>
            <input className='password' value={password} 
            onChange={(event) => setPassword(event.target.value)}
            type='password' placeholder='Пароль'></input>
            <button className='submit-btn' onClick={() => login()} type='submit'>Войти</button>   
            <button className='submit-btn' onClick={() => logout()} type='submit'>Выйти</button>
        </div>
    )
}

export default LoginForm