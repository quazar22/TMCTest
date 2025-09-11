import { useState } from "react";

export default function CreateUserModal({ 
    handleCreateUser, 
    setShowModal }: { 
        handleCreateUser: (e: React.FormEvent, form: { first_name: string; last_name: string; age: string; date_of_birth: string }) => Promise<void>; 
        setShowModal: (show: boolean) => void; 
    }) {

    const [form, setForm] = useState({
            first_name: "",
            last_name: "",
            age: "",
            date_of_birth: "",
        });

    return (
        <dialog className="modal modal-open">
            <div className="modal-box">
                <h3 className="font-bold text-lg mb-4">Add New User</h3>
                <form className="flex flex-col gap-3" onSubmit={(e) => handleCreateUser(e, form)}>
                    <input
                        type="text"
                        placeholder="First Name"
                        className="input input-bordered w-full"
                        value={form.first_name}
                        onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                        required
                    />
                    <input
                        type="text"
                        placeholder="Last Name"
                        className="input input-bordered w-full"
                        value={form.last_name}
                        onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                        required
                    />
                    <input
                        type="number"
                        placeholder="Age"
                        className="input input-bordered w-full"
                        value={form.age}
                        onChange={(e) => setForm({ ...form, age: e.target.value })}
                        required
                    />
                    <input
                        type="datetime-local"
                        placeholder="Date of Birth"
                        className="input input-bordered w-full"
                        value={form.date_of_birth}
                        onChange={(e) =>
                            setForm({ ...form, date_of_birth: e.target.value })
                        }
                        required
                    />
                    <div className="modal-action">
                        <button type="submit" className="btn btn-primary">
                            Save
                        </button>
                        <button
                            type="button"
                            className="btn"
                            onClick={() => setShowModal(false)}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </dialog>
    )
}