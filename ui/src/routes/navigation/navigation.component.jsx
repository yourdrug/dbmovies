import { Outlet } from "react-router-dom";
import Navbar from "../../components/navbar/navbar.component";
import './navigation.styles.css'

const Navigation = () => {

    return(
        <div className="navbar-main">
            <Navbar/>
            <Outlet/>
        </div>
    )
}

export default Navigation;