package domain

import "log"

func CheckErr(err error) {
	if err != nil {
		log.Panicf("Panic! %v", err)
	}
}
