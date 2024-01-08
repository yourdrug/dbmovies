import { Link } from 'react-router-dom';
import Directory from '../../components/directory/directory';
import './home.css'

const Home = () => {
    const categories = [
        {
          id: 1,
          title: 'Фильмы',
          imageUrl: 'https://www.megacritic.ru/images/luchshie-filmy-2021.jpg',
          slug: 'movies'
        },
        {
          id: 2,
          title: 'Сериалы',
          imageUrl: 'https://www.megacritic.ru/images/luchshie-filmy-2021.jpg',
          slug: 'series'
        }
      ];
    
       

    return(
        <div className='main-wrapper'>
            <Directory categories={categories} />
            <div className='album-choices'>
              <Link style={{textDecoration: "none"}}><div className='album-current-choice'>
                ТОП 250
              </div></Link>
              <div className='album-current-choice'>
                ТОП 500
              </div>
            </div>
        </div>
    )
}

export default Home;