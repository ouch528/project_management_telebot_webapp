<template>
    <div>
        <h1>Project Members</h1>
        <ul>
            <li v-for="(name, userId) in memberNames" :key="userId">
                {{ name }}
            </li>
        </ul>
    </div>
</template>

<script>
import { db } from "@/firebase.js"; 
import { doc, getDoc } from "firebase/firestore";

export default {
    data() {
        return {
            memberNames: {},
        };
    },
    async created() {
        const groupHash = this.$route.params.groupHash;

        try {
            const docRef = doc(db, groupHash, "member_names");
            const docSnap = await getDoc(docRef);

            if (docSnap.exists()) {
                this.memberNames = docSnap.data();
            } else {
                console.log("No such document!");
            }
        } catch (e) {
            console.error("Error getting document:", e);
        }
    },
};
</script>