import { UserContext } from "../../context/user.context";
import { useContext, useEffect, useState, useRef } from "react";
import axios from "axios";
import './edit-profile.css'

const EditProfile = () => {

    const { token, currentUser, setCurrentUser } = useContext(UserContext)
    const [selectedImage, setSelectedImage] = useState(currentUser.image);
    const [selectedImageForServer, setSelectedImageForServer] = useState(currentUser.image);

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [new_password, setNewPassword] = useState("")
    const [re_new_password, setReNewPassword] = useState("")
    const [current_password, setCurrentPassword] = useState("")

    const fileInputRef = useRef(null);

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        
        if (file) {
            const formData = new FormData();
            formData.append('image', file);
            setSelectedImageForServer(formData);

            const reader = new FileReader();
            reader.onload = () => {
                setSelectedImage(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleReset = () => {
        setSelectedImage(currentUser.image);
        fileInputRef.current.value = '';
    };

    const handleUploadImage = async () => {
        let config = {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': "Token " + token,
            },
        };
        await axios.patch("http://127.0.0.1:8000/users_update/", selectedImageForServer, config)
    };

    const handleUploadUsername = async () => {
        const data = {
            new_username: username,
            current_password: localStorage.getItem("password")
        }

        const config = {
            headers: {
                'Authorization': "Token " + token,
            },
        };
        await axios.post("http://127.0.0.1:8000/auth/users/set_username/", data, config)
    };

    const handleUploadPassword = async () => {
        const data = {
            new_password: new_password,
            re_new_password: re_new_password,
            current_password: current_password
        }

        const config = {
            headers: {
                'Authorization': "Token " + token,
            },
        };
        await axios.post("http://127.0.0.1:8000/auth/users/set_password/", data, config)
    };

    const handleUploadEmail = async () => {
        const data = {
            email: email
        }

        const config = {
            headers: {
                'Authorization': "Token " + token,
            },
        };
        await axios.patch("http://127.0.0.1:8000/auth/users/me/", data, config)   
    };

    const handleUploadData = async () => {
        if(username){
            await handleUploadUsername();
        }

        if(email){
            await handleUploadEmail();
        }

        if(new_password && re_new_password && current_password){
            await handleUploadPassword();
        }

        if(selectedImage != currentUser.image){
            await handleUploadImage();
        }

        const config = {
            headers: {
                'Authorization': "Token " + token,
            },
        };

        const response = await axios.get("http://127.0.0.1:8000/auth/users/me/", config);
        setCurrentUser(response.data);
        localStorage.setItem("currentUser", JSON.stringify(response.data));
        setUsername("");
        setEmail("");
        setNewPassword("");
        setReNewPassword("");
        setCurrentPassword("");
    };

    useEffect(()=>{

    }, []);


    return (
        <div className="main-wrapper">
            <div className="wrapper-edit-profile">
                <div>
                    {selectedImage && <img src={selectedImage} alt="Selected" onClick={handleReset} width="200" height="200" />}            
                    <input ref={fileInputRef} type="file" accept="image/*" onChange={handleImageChange} />
                </div>
                <div className="inputs-edit-profile">
                    <label>Введите новое имя пользователя</label>
                    <input type="text" placeholder="Имя пользователя" className="current-input-edit-profile"
                        value={username} onChange={(event) => setUsername(event.target.value)}/>
                    <label>Введите новый адрес почты</label>
                    <input type="text" placeholder="example@gmail.com" className="current-input-edit-profile"
                        value={email} onChange={(event) => setEmail(event.target.value)}/>
                    <label>Введите новый пароль</label>
                    <input type="password" value={new_password} className="current-input-edit-profile"
                        onChange={(event) => setNewPassword(event.target.value)}/>
                    <label>Повторите новый пароль</label>
                    <input type="password" value={re_new_password} className="current-input-edit-profile"
                        onChange={(event) => setReNewPassword(event.target.value)}/>
                    <label>Введите текущий пароль</label>
                    <input type="password" value={current_password} className="current-input-edit-profile"
                        onChange={(event) => setCurrentPassword(event.target.value)}/>
                </div>
    
                <button className='control-buttons' onClick={handleUploadData}>Сохранить</button>
            </div>
            
        </div>
        
    );
  };
  
  export default EditProfile;