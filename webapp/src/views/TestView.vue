<template>
    <div>
        <h1>Project Management Dashboard</h1>

        <h2>Team: {{ teamName }}</h2>

        <div>
            <h3>Project Members</h3>
            <ul>
                <li v-for="(name, userId) in memberNames" :key="userId">
                    {{ name }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { db } from '@/firebase'
import { doc, getDoc } from 'firebase/firestore'

const teamName = 'testing' 
const memberNames = ref({})

onMounted(async () => {
    const docRef = doc(db, teamName, 'member_names')
    const docSnap = await getDoc(docRef)

    if (docSnap.exists()) {
        memberNames.value = docSnap.data()
    } else {
        console.warn('No such document!')
    }
})
</script>