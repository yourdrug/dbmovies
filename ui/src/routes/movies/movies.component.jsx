import { useState, useEffect, useContext } from 'react'
import axios from 'axios'
import MovieList from '../../components/movie-list/movie-list.component';
import Pagination from '../../components/pagination-page/pagination-page.component';
import { UserContext } from '../../context/user.context';
import Select from 'react-select';
import './movies.styles.css'

const pageSize = 50;

function Movies() {
  const [myMovies, setMyMovie] = useState([])
  const [page, setPage] = useState(1)
  const [numberOfPages, setNumberOfPages] = useState(1)
  const [selectedGenre, setSelectedGenre] = useState("")
  const [selectedYear, setSelectedYear] = useState("")
  const [selectedCountry, setSelectedCountry] = useState("")
  const [orderingField, setOrderingField] = useState("")
  const [filteredMovies, setFilteredMovies] = useState([])
  
  const { token } = useContext(UserContext) 

  const yearOption = [
    { value: "", label: 'Все года' },
    { value: 2023, label: '2023' },
    { value: 2022, label: '2022' },
    { value: 2021, label: '2021' },
    { value: 2020, label: '2020' },
  ];

  const sortFieldOption = [
    { value: "id", label: 'По порядку' },
    { value: "name", label: 'По названию' },
    { value: "rating", label: 'По рейтингу' },
    { value: "annotated_count_rate", label: 'По количеству оценок' },
  ];

  const genreOption = [
    { value: "", label: 'Все жанры' },
    { value: "драма", label: 'Драма' },
    { value: "боевик", label: 'Боевик' },
    { value: "комедия", label: 'Комедия' },
  ];

  const countryOption = [
    { value: "", label: 'Все страны' },
    { value: "США", label: 'США' },
    { value: "Россия", label: 'Россия' },
    { value: "Великобритания", label: 'Великобритания' },
  ];

  async function getMyMovies(){
    if (token != null){
      var config = {
        headers: {
          Authorization: "Token " + token,
        },
      };
    }
    
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/movie_short/?page=" + page, config
      );
      let movies = await response.data.results;
      let count =  await response.data.count;
      let res = Math.ceil(count / pageSize)
      setNumberOfPages(res);
      setMyMovie(movies);
      setFilteredMovies(movies)
      console.log(token);
      console.log(myMovies);
    } catch (error) {
      alert("ошибка в получении данных с сервера");
    }
  }

  async function getMovies(){
    let config = {
      headers: {
        "X-API-KEY": "3W0ZPKY-H5XM7X8-KRB88NB-QSF7VJ5",
      },
    };
    try {
      for (var k = 1; k < 6; k++){
        console.log("Начинаю получать фильмы с " + k + " страницы");
        const response = await axios.get(
          "https://api.kinopoisk.dev/v1.4/movie?page=" + k + "&limit=50&selectFields=id&selectFields=name&selectFields=names&selectFields=description&selectFields=slogan&selectFields=type&selectFields=year&selectFields=movieLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=persons&selectFields=premiere&notNullFields=id&notNullFields=name&notNullFields=description&notNullFields=slogan&notNullFields=type&notNullFields=year&notNullFields=movieLength&notNullFields=genres.name&notNullFields=countries.name&notNullFields=poster.url&notNullFields=persons.id&notNullFields=persons.name&notNullFields=persons.enName&notNullFields=persons.photo&notNullFields=persons.profession&notNullFields=persons.enProfession&notNullFields=premiere.world&type=movie",
          config
        );
        console.log(response.data.docs);
        for (var i = 0; i < 50; i++){
          console.log("Отправляю " + i + "фильм")
          await postMovie(response.data.docs[i])
          console.log("Загрузил " + i + "фильм")
      }
      }
      
    } catch (error) {
      alert(error.message);
    }
  }

  async function postMovie(movie) {
    let data = {
      movies: movie,
    };
    let config = {
      headers: {
        Authorization: "Token 9adeceea3d89a408b5c8f3157076e756ef9b98ca",
      },
    };
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/movie/addMovies/",
        data,
        config
      );
      console.log(response.status);
    } catch (error) {
      alert(error.message);
    }
  }
  
  function next(){
    setPage(page + 1);
  }

  function filterMovie(){
    let result = myMovies;

    if (selectedGenre) {
      result = result.filter((movie) => movie.genres.some((genre) => genre.name === selectedGenre));
    }

    if (selectedYear) {
      result = result.filter(item => item.year === selectedYear);
    }

    if (selectedCountry) {
      result = result.filter(item => item.country.includes(selectedCountry));
    }

    setFilteredMovies(result);
  }

  function sortMovie(){
    const result = [...filteredMovies];
    result.sort((a, b) => {
      const valueA = a[orderingField];
      const valueB = b[orderingField];

      switch (orderingField){
        case 'id':
          return valueA - valueB;
        case 'name':
          return valueA.localeCompare(valueB);
        case 'rating':
          return valueB - valueA;
        case 'annotated_count_rate':
          return valueB - valueA;
      }});
    setFilteredMovies(result);
  }

  useEffect(()=>{
    getMyMovies();
  }, [page, token]);

  useEffect(()=>{
    filterMovie();
  }, [selectedGenre, selectedYear, selectedCountry, myMovies]);

  useEffect(()=>{
    console.log(orderingField);
    sortMovie();
  }, [orderingField, myMovies]);

  const handleChangeYear = (selectedOption) => {
    setSelectedYear(selectedOption.value);
  };

  const handleChangeSortField = (selectedOption) => {
    setOrderingField(selectedOption.value);
  };

  const handleChangeGenreField = (selectedOption) => {
    setSelectedGenre(selectedOption.value);
  };

  const handleChangeCountryField = (selectedOption) => {
    setSelectedCountry(selectedOption.value);
  };

  return (
    <div className='main-wrapper'>
      <div className='movies-columns'>
        <div>
          <button onClick={getMovies}>Получить фильм</button>
          <button onClick={next}>Следующая страница</button>
          <Pagination setPage={setPage} page={page} numberOfPages={numberOfPages}/>
          <MovieList className='movies-list' movies={filteredMovies} page={page} pageSize={pageSize}/> 
        </div>
        <div>
        <Select className="react-select-container" 
                classNamePrefix="react-select" 
                options={sortFieldOption} 
                defaultValue={sortFieldOption[0]}
                onChange={handleChangeSortField}/>
        <Select className="react-select-container" 
                classNamePrefix="react-select" 
                options={genreOption} 
                defaultValue={genreOption[0]}
                onChange={handleChangeGenreField}/>
        <Select className="react-select-container" 
                classNamePrefix="react-select" 
                options={countryOption} 
                defaultValue={countryOption[0]}
                onChange={handleChangeCountryField}/>
        <Select className="react-select-container" 
                classNamePrefix="react-select" 
                options={yearOption} 
                defaultValue={yearOption[0]}
                onChange={handleChangeYear}/>
        </div>
      </div>
    </div>
  )
}

export default Movies;