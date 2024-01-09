import { Outlet } from "react-router-dom";
import Navbar from "../../components/navbar/navbar";
import './navigation.css'

const Navigation = () => {

    return(
        <div className="navbar-main">
            <Navbar/>
            <Outlet/>
        </div>
    )
}

export default Navigation;