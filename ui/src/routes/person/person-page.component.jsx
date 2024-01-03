import { useState, useEffect } from 'react'
import { useParams, Link } from "react-router-dom";

import axios from 'axios';

import PersonById from "../../components/person-by-id/person-by-id.component";

const PersonPage = () => {
    const [personData, setPersonData] = useState(null)

    const params = useParams();
    let personId = params.id;

    async function getPersonInfo(){
        try {
          const response = await axios.get(
            `http://127.0.0.1:8000/persons/${personId}`);
          let info = await response.data;
          setPersonData(info);
        } catch (error) {
          alert("ошибка в получении данных с сервера");
        }
    }

    useEffect(() => {
        getPersonInfo();
    }, [personId]);

    return(
        <div className="main-wrapper">
            {personData && <PersonById personData={personData} />}
        </div>
    )
}

export default PersonPage;