'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Switch } from "@/components/ui/switch"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { KeyRound, Users, Globe } from 'lucide-react'

const ldapSchema = z.object({
  enabled: z.boolean(),
  serverUrl: z.string().url().optional(),
  bindDN: z.string().optional(),
  bindPassword: z.string().optional(),
  searchBase: z.string().optional(),
  searchFilter: z.string().optional(),
})

const adSchema = z.object({
  enabled: z.boolean(),
  domain: z.string().optional(),
  serverUrl: z.string().url().optional(),
  username: z.string().optional(),
  password: z.string().optional(),
})

const ssoSchema = z.object({
  enabled: z.boolean(),
  provider: z.enum(['azure', 'okta', 'google']),
  clientId: z.string().optional(),
  clientSecret: z.string().optional(),
  tenantId: z.string().optional(),
})

export function AuthSettings() {
  const [activeProvider, setActiveProvider] = useState<'ldap' | 'ad' | 'sso'>('ldap')

  const ldapForm = useForm({
    resolver: zodResolver(ldapSchema),
    defaultValues: {
      enabled: false,
      serverUrl: '',
      bindDN: '',
      bindPassword: '',
      searchBase: '',
      searchFilter: '',
    },
  })

  const adForm = useForm({
    resolver: zodResolver(adSchema),
    defaultValues: {
      enabled: false,
      domain: '',
      serverUrl: '',
      username: '',
      password: '',
    },
  })

  const ssoForm = useForm<z.infer<typeof ssoSchema>>({
    resolver: zodResolver(ssoSchema),
    defaultValues: {
      enabled: false,
      provider: 'azure',
      clientId: '',
      clientSecret: '',
      tenantId: '',
    },
  })

  const onLDAPSubmit = async (data: z.infer<typeof ldapSchema>) => {
    try {
      const response = await fetch('/api/auth/ldap', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to update LDAP settings')
      // Handle success
    } catch (error) {
      console.error('Error updating LDAP settings:', error)
    }
  }

  const onADSubmit = async (data: z.infer<typeof adSchema>) => {
    try {
      const response = await fetch('/api/auth/active-directory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to update AD settings')
      // Handle success
    } catch (error) {
      console.error('Error updating AD settings:', error)
    }
  }

  const onSSOSubmit = async (data: z.infer<typeof ssoSchema>) => {
    try {
      const response = await fetch('/api/auth/sso', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to update SSO settings')
      // Handle success
    } catch (error) {
      console.error('Error updating SSO settings:', error)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex space-x-4">
        <Button
          variant={activeProvider === 'ldap' ? 'default' : 'outline'}
          onClick={() => setActiveProvider('ldap')}
          className="flex items-center gap-2"
        >
          <KeyRound className="h-4 w-4" />
          LDAP
        </Button>
        <Button
          variant={activeProvider === 'ad' ? 'default' : 'outline'}
          onClick={() => setActiveProvider('ad')}
          className="flex items-center gap-2"
        >
          <Users className="h-4 w-4" />
          Active Directory
        </Button>
        <Button
          variant={activeProvider === 'sso' ? 'default' : 'outline'}
          onClick={() => setActiveProvider('sso')}
          className="flex items-center gap-2"
        >
          <Globe className="h-4 w-4" />
          Single Sign-On
        </Button>
      </div>

      {activeProvider === 'ldap' && (
        <Card className="bg-gray-900/50 border-gray-800">
          <CardHeader>
            <CardTitle className="text-gray-100">LDAP Configuration</CardTitle>
            <CardDescription className="text-gray-400">
              Configure LDAP authentication settings for your organization.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...ldapForm}>
              <form onSubmit={ldapForm.handleSubmit(onLDAPSubmit)} className="space-y-4">
                <FormField
                  control={ldapForm.control}
                  name="enabled"
                  render={({ field }) => (
                    <FormItem className="flex items-center justify-between rounded-lg border border-gray-800 p-4">
                      <div className="space-y-0.5">
                        <FormLabel className="text-base">Enable LDAP Authentication</FormLabel>
                        <FormDescription>
                          Allow users to sign in using LDAP credentials
                        </FormDescription>
                      </div>
                      <FormControl>
                        <Switch
                          checked={field.value}
                          onCheckedChange={field.onChange}
                        />
                      </FormControl>
                    </FormItem>
                  )}
                />
                <FormField
                  control={ldapForm.control}
                  name="serverUrl"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Server URL</FormLabel>
                      <FormControl>
                        <Input placeholder="ldap://example.com:389" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={ldapForm.control}
                    name="bindDN"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Bind DN</FormLabel>
                        <FormControl>
                          <Input placeholder="cn=admin,dc=example,dc=com" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={ldapForm.control}
                    name="bindPassword"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Bind Password</FormLabel>
                        <FormControl>
                          <Input type="password" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={ldapForm.control}
                    name="searchBase"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Search Base</FormLabel>
                        <FormControl>
                          <Input placeholder="dc=example,dc=com" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={ldapForm.control}
                    name="searchFilter"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Search Filter</FormLabel>
                        <FormControl>
                          <Input placeholder="(uid=%s)" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <Button type="submit">Save LDAP Settings</Button>
              </form>
            </Form>
          </CardContent>
        </Card>
      )}

      {activeProvider === 'ad' && (
        <Card className="bg-gray-900/50 border-gray-800">
          <CardHeader>
            <CardTitle className="text-gray-100">Active Directory Configuration</CardTitle>
            <CardDescription className="text-gray-400">
              Configure Active Directory authentication settings.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...adForm}>
              <form onSubmit={adForm.handleSubmit(onADSubmit)} className="space-y-4">
                <FormField
                  control={adForm.control}
                  name="enabled"
                  render={({ field }) => (
                    <FormItem className="flex items-center justify-between rounded-lg border border-gray-800 p-4">
                      <div className="space-y-0.5">
                        <FormLabel className="text-base">Enable Active Directory</FormLabel>
                        <FormDescription>
                          Allow users to sign in using Active Directory credentials
                        </FormDescription>
                      </div>
                      <FormControl>
                        <Switch
                          checked={field.value}
                          onCheckedChange={field.onChange}
                        />
                      </FormControl>
                    </FormItem>
                  )}
                />
                <FormField
                  control={adForm.control}
                  name="domain"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Domain</FormLabel>
                      <FormControl>
                        <Input placeholder="example.com" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={adForm.control}
                  name="serverUrl"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Server URL</FormLabel>
                      <FormControl>
                        <Input placeholder="ldap://dc.example.com" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={adForm.control}
                    name="username"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Service Account Username</FormLabel>
                        <FormControl>
                          <Input {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={adForm.control}
                    name="password"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Service Account Password</FormLabel>
                        <FormControl>
                          <Input type="password" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <Button type="submit">Save AD Settings</Button>
              </form>
            </Form>
          </CardContent>
        </Card>
      )}

      {activeProvider === 'sso' && (
        <Card className="bg-gray-900/50 border-gray-800">
          <CardHeader>
            <CardTitle className="text-gray-100">Single Sign-On Configuration</CardTitle>
            <CardDescription className="text-gray-400">
              Configure SSO provider settings for your organization.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...ssoForm}>
              <form onSubmit={ssoForm.handleSubmit(onSSOSubmit)} className="space-y-4">
                <FormField
                  control={ssoForm.control}
                  name="enabled"
                  render={({ field }) => (
                    <FormItem className="flex items-center justify-between rounded-lg border border-gray-800 p-4">
                      <div className="space-y-0.5">
                        <FormLabel className="text-base">Enable SSO</FormLabel>
                        <FormDescription>
                          Allow users to sign in using Single Sign-On
                        </FormDescription>
                      </div>
                      <FormControl>
                        <Switch
                          checked={field.value}
                          onCheckedChange={field.onChange}
                        />
                      </FormControl>
                    </FormItem>
                  )}
                />
                <FormField
                  control={ssoForm.control}
                  name="provider"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>SSO Provider</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select a provider" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="azure">Azure AD</SelectItem>
                          <SelectItem value="okta">Okta</SelectItem>
                          <SelectItem value="google">Google Workspace</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={ssoForm.control}
                    name="clientId"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Client ID</FormLabel>
                        <FormControl>
                          <Input {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={ssoForm.control}
                    name="clientSecret"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Client Secret</FormLabel>
                        <FormControl>
                          <Input type="password" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <FormField
                  control={ssoForm.control}
                  name="tenantId"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Tenant ID</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <Button type="submit">Save SSO Settings</Button>
              </form>
            </Form>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

