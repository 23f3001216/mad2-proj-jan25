import { createRouter, createWebHistory } from 'vue-router';

// Public Components
import MainPage from '@/components/MainPage.vue';
import UserLoginPage from '@/components/UserLoginPage.vue';
import UserSignUpPage from '@/components/UserSignUpPage.vue';
import AdminLoginPage from '@/components/AdminLoginPage.vue';

// User Components
import UserHomePage from '@/components/UserHomePage.vue';
import UserSummaryPage from '@/components/UserSummaryPage.vue';
import UserEditProfilePage from '@/components/UserEditProfilePage.vue';

// Admin Components
import AdminHomePage from '@/components/AdminHomePage.vue';
import AdminUsersPage from '@/components/AdminUsersPage.vue';
import AdminSearchPage from '@/components/AdminSearchPage.vue';
import AdminSummaryPage from '@/components/AdminSummaryPage.vue';
import AdminEditProfilePage from '@/components/AdminEditProfilePage.vue'

// Layout
import UserLayout from '@/layouts/UserLayout.vue';
import AdminLayout from '@/layouts/AdminLayout.vue';

const routes = [
    {
        path: '/',
        name: 'MainPage',
        component: MainPage,
    },
    {
        path: '/user-login',
        name: 'Login',
        component: UserLoginPage,
    },
    {
        path: '/user-signup',
        name: 'SignUp',
        component: UserSignUpPage,
    },
    {
        path: '/admin-login',
        name: 'AdminLogin',
        component: AdminLoginPage,
    },

    // USER ROUTES (Protected)
    {
        path: '/user',
        component: UserLayout,
        meta: { requiresAuth: true, role: 'user' },
        children: [
            {
                path: '',
                redirect: 'home',
            },
            {
                path: 'home',
                name: 'UserHome',
                component: UserHomePage,
            },
            {
                path: 'summary',
                name: 'UserSummary',
                component: UserSummaryPage,
            },
            {
                path: 'edit-profile',
                name: 'UserEditProfile',
                component: UserEditProfilePage,
            },
        ],
    },

    // ADMIN ROUTES (Protected)
    {
        path: '/admin',
        component: AdminLayout,
        meta: { requiresAuth: true, role: 'admin' },
        children: [
            {
                path: '',
                redirect: 'home',
            },
            {
                path: 'home',
                name: 'AdminHome',
                component: AdminHomePage,
            },
            {
                path: 'users',
                name: 'AdminUsers',
                component: AdminUsersPage,
            },
            {
                path: 'search',
                name: 'AdminSearch',
                component: AdminSearchPage,
            },
            {
                path: 'summary',
                name: 'AdminSummary',
                component: AdminSummaryPage,
            },
            {
                path: 'edit-profile',
                name: 'AdminEditProfile',
                component: AdminEditProfilePage,
            },
        ],
    },

    // Fallback route
    {
        path: '/:pathMatch(.*)*',
        redirect: '/',
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// --- GLOBAL ROUTE GUARD ---
router.beforeEach((to, from, next) => {
    const isLoggedIn = !!localStorage.getItem('role');
    const role = localStorage.getItem('role'); // 'user' or 'admin'

    if (to.meta.requiresAuth) {
        if (!isLoggedIn) {
            // Not logged in, redirect based on the expected role
            if (to.meta.role === 'admin') return next('/admin-login');
            return next('/user-login'); // default to user login
        }

        // Logged in, but trying to access a route not meant for their role
        if (to.meta.role && to.meta.role !== role) {
            return next('/');
        }
    }

    next(); // allow navigation
});


export default router;
