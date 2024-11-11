from fastapi import HTTPException, status


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

WrongPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Wrong password",
)

UnauthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is not authorized"
)
