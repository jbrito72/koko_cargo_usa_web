import { Box, Container, Heading, Text } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"

import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/")({
  component: Home,
})

function Home() {
  const { user: currentUser } = useAuth()

  return (
    <Container maxW="full">
      <Box pt={12} m={4}>
        <Heading size="xl" mb={4}>
          Sistema de Gestión
        </Heading>
        <Text fontSize="lg" mb={2}>
          Bienvenido, {currentUser?.full_name || currentUser?.email}
        </Text>
        <Text color="gray.600">
          Sistema de gestión para camaroneras
        </Text>
      </Box>
    </Container>
  )
}
