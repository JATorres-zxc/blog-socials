<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Edit profile</h1>
                <RouterLink to="/profile/edit/password" class="underline">Edit password</RouterLink>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>Name</label><br>
                        <input type="text" v-model="form.name" placeholder="Your full name" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <!-- for attach image shit js below -->
                    <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                        <input type="file" ref="file" @change="handleFileChange">
                        <!-- fileName sa js below -->
                        <span v-if="fileName" class="text-sm text-gray-300">{{ fileName }}</span>
                        <span v-else>Change Avatar</span>
                    </label>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<!-- style for attach image button -->
<style>
    input[type='file']{
        display: none;
    }

    .custom-file-upload{
        border: 1px solid #ccc;
        display: inline-block;
        padding: 6px 12px;
        cursor: pointer;
    }
</style>

<script>
import axios from 'axios'

import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        // Access toast store and user store
        const toastStore = useToastStore()
        const userStore = useUserStore()

        return {
            toastStore,
            userStore
        }
    },

    // Data for component
    data() {
        return {
            // Initialize form with user data
            form: {
                email: this.userStore.user.email,
                name: this.userStore.user.name,
                avatar:null
            },
            errors: [],
        }
    },

    // Methods for component
    methods: {
        // Method to handle form submission
        submitForm() {
            // Clear previous errors
            this.errors = []

            // Check if email is missing
            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            // Check if name is missing
            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }

            // If no errors, proceed with form submission
            if (this.errors.length === 0) {
                // Create form data
                let formData = new FormData()
                formData.append('avatar', this.$refs.file.files[0])
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)

                // Submit form data
                axios
                    .post('/api/editprofile/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        // If information update is successful
                        if (response.data.message === 'information updated') {
                            // Show success toast message
                            this.toastStore.showToast(5000, 'The information was saved', 'bg-emerald-500')

                            // Update user information in user store
                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email,
                                avatar: response.data.user.get_avatar
                            })

                            // Navigate back to previous page
                            this.$router.back()
                        } else {
                            // If there are errors, show error toast message
                            this.toastStore.showToast(5000, `${response.data.message}. Please try again`, 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        // Log error if request fails
                        console.log('error', error)
                    })
            }
        },
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                // Update fileName with selected file name
                this.fileName = file.name;
            } else {
                this.fileName = null;
            }
        },
    }
}
</script>
