import { useState, useContext, useEffect } from 'react'
import axios from 'axios'
import './login-form.css'
import { UserContext } from '../../context/user.context'

const LoginForm = ({setActive}) =>{
    const [password, setPassword] = useState("")
    const [username, setUsername] = useState("")

    const [reg_password, setRegPassword] = useState("")
    const [reg_re_password, setRegRePassword] = useState("")
    const [reg_username, setRegUsername] = useState("")
    const [isLoginFormVisible, setLoginFormVisible] = useState(true);

    const { currentUser, setCurrentUser, setToken, token } = useContext(UserContext) 

    async function getAccountInfo(token) {
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
          localStorage.setItem("currentUser", JSON.stringify(response.data));
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
          localStorage.setItem("token", response.data.auth_token);
          localStorage.setItem("password", password);
          setToken(response.data.auth_token);
          await getAccountInfo(response.data.auth_token);
          setActive(false);
        } catch (error) {
          alert(error.message);
        }
    }

    async function signUp() {
      let data = { username: reg_username, password: reg_password };
      console.log(reg_password);
      try {
        const response = await axios.post("http://127.0.0.1:8000/auth/users/", data);
        console.log(response);
      } catch (error) {
        alert(error.message);
      }
  }

    return(
        <div className='login-from'> 
            <div className="wrapper-for-login-form">
              <div className={`form-box-login-${isLoginFormVisible ? 'active' : 'not-active'}`}>
                <h2>Войти</h2>
                <div>
                  <div className="input-box">
                    <input type="text" required  value={username} 
                      onChange={(event) => setUsername(event.target.value)}/>
                    <label>Имя пользователя</label>
                  </div>
                  <div className="input-box">
                    <input type="password" required value={password} 
                      onChange={(event) => setPassword(event.target.value)}/>
                    <label>Пароль</label>
                  </div>
                  <div className="remember-forgot">
                    <label><input type="checkbox" />Запомнить меня</label>
                  </div>
                  <button onClick={login} type="submit" className="login-btn-for-form">Войти</button>
                  <div className="login-register">
                    <p>
                      Нет аккаунта?&nbsp;
                      <span onClick={()=>setLoginFormVisible(false)} className="register-link">Регистрация</span>
                    </p>
                  </div>
                </div>
              </div>
              <div className={`form-box-register-${isLoginFormVisible ? 'not-active' : 'active'}`}>
                <h2>Регистрация</h2>
                <div>
                  <div className="input-box">
                    <input className="username" type="text" required value={reg_username} 
                      onChange={(event) => setRegUsername(event.target.value)}/>
                    <label>Имя пользователя</label>
                  </div>
                  <div className="input-box">
                    <input className="password" type="password" required value={reg_password} 
                      onChange={(event) => setRegPassword(event.target.value)}/>
                    <label>Пароль</label>
                  </div>
                  <div className="input-box">
                    <input className="password" type="password" required value={reg_re_password} 
                      onChange={(event) => setRegRePassword(event.target.value)}/>
                    <label>Повторите пароль</label>
                  </div>
                  <div className="remember-forgot">
                    <label><input type="checkbox" />Я согласен с условиями и правилами</label>
                  </div>
                  <button onClick={signUp} type="submit" className="login-btn-for-form">Зарегистрироваться</button>
                  <div className="login-register">
                    <p>
                      Уже есть аккаунт?&nbsp;
                      <span onClick={()=>setLoginFormVisible(true)} className="register-link">Войти</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
    )
}

export default LoginForm;