def login():
  
    with PGSession() as session:
        stmt = select(Users).where(Users.role)
        
        res:List[Users] = session.execute(stmt).scalars().all()
        for i in res:
            print(i.title)





    if Users:
        messagebox.showinfo("Успех", f"Вход выполнен! Ваша роль: {Users.role}")
        root.destroy()

        if Users.role == "superadmin":
            SuperAdminPanel()
        elif Users.role == "admin":
            AdminPanel()
        elif Users.role == "user":
            UserPanel()
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")
