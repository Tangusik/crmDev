import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Header from "../components/Header";
import Footer from "../components/Footer";
import Button from "../components/Button";
import ClientCard from "../components/ClientCard";
import styles from "./index.module.css";
import EditModal from "../components/EditModal";
import Form from "../components/Form";
import {fetchGet} from "../api/get";
import {fetchPost} from "../api/post";

const Clients = () => {
    const [clients, setClients] = useState([]);
    const [chosenClientState, setChosenClientState] = useState([]);
    const [clientsStates, setClientsStates] = useState([]);

    const [showModalAllClients, setShowModalAllClients] = useState(false);
    const [showModalGroups, setShowModalGroups] = useState(false);

    const [showModalAddClient, setShowModalAddClient] = useState(false);
    const [showModalAddGroup, setShowModalAddGroup] = useState(false);

    const [firstName, setFirstName] = useState([]);
    const [lastName, setLastName] = useState([]);
    const [birthDate, setBirthDate] = useState([]);
    const [balance, setBalance] = useState([]);

    const handleAllClients = () => {
        setShowModalAllClients(!showModalAllClients);
    }
    const handleGroups = () => {
        setShowModalGroups(!showModalGroups);
    }

    const handleAddClient = () => {
        setShowModalAddClient(!showModalAddClient);
    }
    const handleAddGroup = () => {
        setShowModalAddGroup(!showModalAddGroup);
    }

    useEffect( () => {
        const fetchData = async () => {
            const response = await fetchGet('client_list');
            setClients(response);

            const clientsStates = await fetchGet('cl_statuses');
            setClientsStates(clientsStates)
        }

        fetchData();
    }, []);

    const handleFetchAddClient = async (event) => {
        event.preventDefault();

        const data = {
            first_name: firstName,
            last_name: lastName,
            birth_date: birthDate,
            state: chosenClientState,
            balance: balance,
        };
        await fetchPost( 'add_client', data);
        setShowModalAddClient(false)
        window.location.reload();
    };

    return (
        <div>
            <Header></Header>
            <div className={styles.mainContent}>
                <div className={styles.buttons}>
                    <Button type={"main"} title={"Все клиенты"} onClick={handleAllClients}></Button>
                    <Button type={"main"} title={"Группы"} onClick={handleGroups}></Button>
                </div>
                {showModalAllClients ? (
                    <div>
                        <span style={{  display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                            <Button type={"change"} title={"Добавить клиента"} onClick={handleAddClient}></Button>
                        </span>
                        <div className={styles.cards}>
                            {clients.length===0 && <p>Нет клиентов</p>}
                            {clients.map((client) => (
                                <ClientCard
                                    key={client.id}
                                    id={client.id}
                                    firstName={client.first_name}
                                    lastName={client.last_name}
                                    birthday={client.birth_date}
                                    state={client.state}
                                    balance={client.balance}
                                >
                                </ClientCard>
                            ))}
                        </div>
                    </div>
                ):(
                    <div></div>
                )}
                {showModalAddClient &&
                    <EditModal
                        onClose={handleAddClient}
                        children={
                            <Form
                                onSubmit={handleFetchAddClient}
                                title={'Добавление клиента'}
                                children={
                                    <div>
                                        <input type="text" name="first_name" id="first_name" placeholder="Имя" onChange={(e) => setFirstName(e.target.value)}/>
                                        <input type="text" name="last_name" id="last_name" placeholder="Фамилия" onChange={(e) => setLastName(e.target.value)}/>
                                        <input type="date" name="birth_date" id="birth_date" placeholder="Дата рождения" onChange={(e) => setBirthDate(e.target.value)}/>
                                        <input type="text" name="balance" id="balance" placeholder="Баланс" onChange={(e) => setBalance(e.target.value)}/>
                                        <select id="state" required name="state" className={styles.select} onChange={(e) => setChosenClientState(e.target.value)}>
                                            {clientsStates.map((state)=>
                                                (<option key={state.id} value={state.id}>{state.name}</option>)
                                            )}
                                        </select>
                                        <input type="submit" value="Добавить"/>
                                    </div>}
                            ></Form>}>
                    </EditModal>
                }
                {showModalGroups ? (
                    <div>
                         <span style={{  display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                            <Button type={"change"} title={"Добавить группу"} onClick={handleAddGroup}></Button>
                         </span>
                    </div>
                ):(
                    <div></div>
                )}
                {showModalAddGroup &&
                    <EditModal
                        onClose={handleAddGroup}
                        children={
                            <Form
                                title={'Добавление группы'}
                                children={
                                    <div>
                                        <input type="text" id="name" name="title" placeholder="Название"/>
                                            <p>
                                                <select multiple name="members" className="select">
                                                    <option value="{{client.id}}"></option>
                                                </select>
                                            </p>
                                            <p>Тренер:</p>
                                            <p>
                                                <select name="trainer" className="select">
                                                    <option value="{{trainer.user.id}}"></option>
                                                </select>
                                            </p>
                                            <p>
                                                <select name="sport_type" className="select">
                                                    <option value="{{type.id}}"></option>
                                                </select>
                                            </p>
                                            <p>
                                                <select name="area" className="select">
                                                    <option value="{{area.id}}"></option>
                                                </select>
                                            </p>
                                            <p>Занятия:</p>
                                            <p>До какого числа будут проходить занятия: <input type="date" name="date_end"/></p>
                                            <p>Дни недели:
                                                <select multiple name="days" className="select">
                                                    <option value="0">Понедельник</option>
                                                    <option value="1">Вторник</option>
                                                    <option value="2">Среда</option>
                                                    <option value="3">Четверг</option>
                                                    <option value="4">Пятница</option>
                                                    <option value="5">Суббота</option>
                                                    <option value="6">Воскресенье</option>
                                                </select></p>
                                            <input type="time" name="act_begin_time" placeholder="Время начала занятий"/>
                                            <input type="time" name="act_end_time" placeholder="Время конца занятий"/>
                                            <input type="submit" value="Добавить"/>
                                    </div>}
                            ></Form>}
                    ></EditModal>
                }
            </div>
            <Footer></Footer>
        </div>
    );
}

export default Clients;
