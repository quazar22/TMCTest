"use client";

import CreateUserModal from "@/components/CreateUserModal";
import { useEffect, useState } from "react";

const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);

    async function fetchUsers() {
        try {
            setLoading(true);
            const res = await fetch(`${NEXT_PUBLIC_API_URL}/users/`);
            if (!res.ok) {
                throw new Error("Failed to fetch users");
            }
            const data = await res.json();
            setUsers(data);
        } catch (error) {
            console.error("Error fetching users:", error);
        } finally {
            setLoading(false);
        }
    }

    async function handleCreateUser(e: React.FormEvent | undefined, form: UserForm) {
        e?.preventDefault();
        const newUser = {
            first_name: form.first_name,
            last_name: form.last_name,
            age: parseInt(form.age, 10),
            date_of_birth: form.date_of_birth,
        };
        await fetch(`${NEXT_PUBLIC_API_URL}/user/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newUser),
        });
        setShowModal(false);
        fetchUsers();
    }

    async function createTestUser() {
        const testUser: UserForm = {
            first_name: "Test",
            last_name: "User",
            age: "30",
            date_of_birth: "1993-01-01",
        };
        await handleCreateUser(undefined, testUser);
    }

    async function deleteUser(id: number) {
        await fetch(`${NEXT_PUBLIC_API_URL}/user/${id}`, {
            method: "DELETE",
        });
        setUsers((prev) => prev.filter((u) => u.id !== id));
    }

    useEffect(() => {
        fetchUsers();
    }, []);

    return (
        <div className="p-8 min-h-screen bg-base-200">
            <h1 className="text-2xl font-bold mb-6">User Management</h1>

            <div>
                <button className="btn btn-primary mb-4" onClick={() => setShowModal(true)}>
                    Add User
                </button>
                <button className="btn btn-primary mb-4 ml-4" onClick={createTestUser}>
                    Add Test User
                </button>
            </div>

            {showModal && (
                <CreateUserModal handleCreateUser={handleCreateUser} setShowModal={setShowModal} />
            )}

            {loading ? (
                <div className="loading loading-spinner loading-lg"></div>
            ) : (
                <div className="overflow-x-auto w-full">
                    <table className="table table-zebra w-full">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Age</th>
                                <th>Date of Birth</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users && users.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="text-center">
                                        No users found
                                    </td>
                                </tr>
                            ) : (
                                users.map((user) => (
                                    <tr key={user.id}>
                                        <td>{user.id}</td>
                                        <td>
                                            {user.first_name} {user.last_name}
                                        </td>
                                        <td>{user.age}</td>
                                        <td>
                                            {new Date(user.date_of_birth).toLocaleDateString()}
                                        </td>
                                        <td>
                                            <button
                                                className="btn btn-error btn-sm"
                                                onClick={() => deleteUser(user.id)}
                                            >
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
