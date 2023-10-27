import StartPage from "@/pages/StartPage";
import MoviesPage from "@/pages/MoviesPage";
import MovieIdPage from "@/pages/MovieIdPage";
import MovieByGenre from "@/pages/MovieByGenre";
import DirectorIdPage from "@/pages/DirectorIdPage";
import ActorIdPage from "@/pages/ActorIdPage";
import ProducerIdPage from "@/pages/ProducerIdPage";
import ScreenwriterIdPage from "@/pages/ScreenwriterIdPage";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {
        path: '/',
        component: StartPage
    },
    {
        path: '/movies',
        component: MoviesPage
    },
    {
        path: '/movies/:id',
        component: MovieIdPage
    },
    {
        path: '/movies/by-genre/:genre',
        component: MovieByGenre
    },
    {
        path: '/persons/director/:id',
        component: DirectorIdPage
    },
    {
        path: '/persons/actor/:id',
        component: ActorIdPage
    },
    {
        path: '/persons/screenwriter/:id',
        component: ScreenwriterIdPage
    },
    {
        path: '/persons/producer/:id',
        component: ProducerIdPage
    },
]

const router = createRouter({
    routes,
    history: createWebHistory(process.env.BASE_URL)
})

export default router;