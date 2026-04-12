import { useEffect, type ReactNode } from "react";
import { useAuthStore } from "../modules/auth/state/auth.store";

type AppProvidersProps = {
	children: ReactNode;
};

export function AppProviders({ children }: AppProvidersProps) {
	const hydrate = useAuthStore((state) => state.hydrate);

	useEffect(() => {
		hydrate();
	}, [hydrate]);

	return <>{children}</>;
}
