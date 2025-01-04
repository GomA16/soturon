"use client";

export const Button = ({children}:{children:React.ReactNode}) => {
    return (
        <>
        <button className="bg-blue-500 rounded hover:bg-blue-700">{children}</button>
      </>
      )
}