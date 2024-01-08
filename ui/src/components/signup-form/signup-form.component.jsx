import { useState, useContext, useEffect } from 'react'
import axios from 'axios'
import './signup-form.styles.css'
import { UserContext } from '../../context/user.context'

const SignUpForm = () =>{
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [rePassword, setRePassword] = useState("")

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
          localStorage.setItem("currentUser", JSON.stringify(response.data));
          setCurrentUser(response.data);
          console.log(response);
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
          localStorage.setItem("token", response.data.auth_token);
        } catch (error) {
          alert(error.message);
        }
    }

    async function signUp() {
        let data = { username: username, password: password};
        console.log(password);
        try {
          const response = await axios.post(
            "http://127.0.0.1:8000/auth/users/",
            data
          );
          console.log(response);
        } catch (error) {
          alert(error.message);
        }
    }

    useEffect(() => {
        if (token !== null) {
            getAccountInfo();
        }
    }, [token]);

    return(
        <div className='login-from'>
            <h1 className='title'>Введите поля для регистрации</h1>
            <input className='username' value={username} 
            onChange={(event) => setUsername(event.target.value)} 
            type='text' placeholder='Имя пользователя'/>
            <input className='password' value={password} 
            onChange={(event) => setPassword(event.target.value)}
            type='password' placeholder='Пароль'></input>
            <input className='password' value={rePassword} 
            onChange={(event) => setRePassword(event.target.value)}
            type='password' placeholder='Повторите пароль'></input>
            <button className='submit-btn' onClick={() => login()} type='submit'>Войти</button>
            <button className='submit-btn' onClick={() => signUp()} type='submit'>Регистрация</button>   
        </div>
    )
}

export default SignUpForm