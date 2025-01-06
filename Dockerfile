# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /source

# Copy csproj and restore as distinct layers
COPY BlogApi/BlogApi.csproj ./BlogApi/
RUN dotnet restore ./BlogApi/BlogApi.csproj --packages ./

# Copy the rest of the source code and build the app
COPY BlogApi/. ./BlogApi/
WORKDIR /source/BlogApi
RUN dotnet publish -c Release -o /app --packages ./

# Stage 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app ./
EXPOSE 5000
ENTRYPOINT ["dotnet", "Api.dll", "--urls", "http://0.0.0.0:5000"]
